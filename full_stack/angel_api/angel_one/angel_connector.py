# package import statement
import json
import os
import time
from datetime import datetime

import pandas as pd
import pyotp
import requests
from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect
from pytz import timezone

from angel_one.configs import MASTER_FILE_PATH, ORDER_MARKET, PRODCUT_TYPE_CARRY_FORWARD, \
    TYPE_SELL, MASTER_FILE, VARIETY_NORMAL, XCHANGE_NSE, INTERVAL_5_MIN
from angel_one.token_ids import APP_TOKEN_KEY, USERNAME, LOGIN_CODE, API_KEY
from common_utils.log_utils import LogUtils

STATUS = 'status'
DATA = 'data'


class AngelConnector():

    def __init__(self):
        self.logger_obj = LogUtils.return_logger(__name__)
        print('constructor')

    def prepare_master_df(self):
        dt_now = datetime.now(timezone("Asia/Kolkata"))
        file_name = MASTER_FILE_PATH.format(dt_now.strftime('%Y-%m-%d'))

        if os.path.isfile(file_name):
            self.logger_obj.info(f"JSON file is already available : {file_name}")
        else:
            try:

                # Send a GET request to the URL
                response = requests.get(MASTER_FILE, verify=False)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse JSON content from the response
                    json_content = response.json()
                    # Save the JSON content to a local file
                    with open(file_name, 'w') as f:
                        json.dump(json_content, f)  # Save JSON content with indentation

                    self.logger_obj.info(f"JSON file downloaded successfully and saved as: {file_name}")
                else:
                    self.logger_obj.error(f"Failed to download JSON file. Status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error downloading JSON file: {e}")

        df = pd.read_json(file_name)

        df.reset_index(level=0, inplace=True)
        self.logger_obj.info('Loaded master {} data successfully .'.format(df.size))
        # master_df[master_df['symbol'].str.contains('NIFTY10APR2423000CE') == True]
        self.master_df = df

    def generate_smart_api_session(self):
        try:
            self.prepare_master_df()

            self.smartApi = SmartConnect(API_KEY, disable_ssl=True)
            totp = pyotp.TOTP(APP_TOKEN_KEY).now()

        except Exception as e:
            self.logger_obj.error("Invalid Token: The provided token is not valid.")
            raise e

        correlation_id = "abcde"
        data = self.smartApi.generateSession(USERNAME, LOGIN_CODE, totp)

        if data['status'] == False:
            self.logger_obj.error(data)
            exit(1)

        pass

        # login api call
        # logger.info(f"You Credentials: {data}")
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        # fetch the feedtoken
        feedToken = self.smartApi.getfeedToken()
        # fetch User Profile
        res = self.smartApi.getProfile(refreshToken)
        self.smartApi.generateToken(refreshToken)
        res = res['data']['exchanges']
        return self.smartApi

    def get_holdings(self, filters=None):
        return self.smartApi.holding()

    def get_orders(self, filters=None):
        orders = self.smartApi.orderBook()
        i = 1
        while orders.get('errorcode') :
            self.logger_obj.error('get_orders failed: {}'.format(orders))
            time.sleep(i)
            orders = self.smartApi.orderBook()
            i += 1
        return orders

    def get_positions(self, filters=None):
        postns = self.smartApi.position()
        i = 1
        while postns.get('errorcode'):
            self.logger_obj.error('get_positions failed: {}'.format(postns))
            time.sleep(i)
            postns = self.smartApi.position()
            i += 1
        return postns

    def get_script_details(self, script_name):
        row = self.master_df[self.master_df['symbol'].str.contains(script_name) == True]
        if row.size > 0:
            return row.to_dict(orient='records')[0]

        self.logger_obj.info('Script {} not found in master file.'.format(script_name))
        return None

    def get_ltp(self, my_exchange='NSE', my_symbol='', my_token='3045', ):
        # my_symbol is not used, only exchange and token are considered, 3045-SBI-EQ
        ltp = self.smartApi.ltpData(my_exchange, my_symbol, my_token)
        i = 1
        while ltp.get('errorcode'):
            self.logger_obj.error('get_ltp failed: {}'.format(ltp))
            time.sleep(i)
            ltp = self.smartApi.ltpData(my_exchange, my_symbol, my_token)
            i += 1
        return ltp
        # return self.smartApi.ltpData(my_exchange, my_symbol, my_token)

    def get_candlde_data(self, my_exchange=XCHANGE_NSE, my_token='3045', my_interval=INTERVAL_5_MIN, ):
        # https://smartapi.angelbroking.com/docs/Historical
        try:
            # historicParam = {
            #     "exchange": "NSE",
            #     "symboltoken": "3045",
            #     "interval": "ONE_MINUTE",
            #     "fromdate": "2024-04-01 09:15",
            #     "todate": "2024-08-01 09:30"
            # }

            historicParam = {
                "exchange": my_exchange,
                "symboltoken": my_token,
                "interval": my_interval,
                "fromdate": "{} 09:15".format(datetime.now().strftime('%Y-%m-%d')),
                "todate": "{} 15:30".format(datetime.now().strftime('%Y-%m-%d')),
            }

            op = self.smartApi.getCandleData(historicParam)
            return op.get(DATA) if op.get(STATUS) else None


        except Exception as e:
            print("Historic Api failed: {}".format(e.message))

    def order_placment(self, my_symbol='SBIN-EQ', my_token='3045', my_type=TYPE_SELL, my_exchange='NSE', my_price=1,
                       my_quantity=1, my_order_type=ORDER_MARKET, my_ordertag='', my_variety = VARIETY_NORMAL,
                       my_product_type= PRODCUT_TYPE_CARRY_FORWARD, my_squar_off= '0', my_stop_loss= '0'):
        try:
            # orderparams = {
            #     "variety": "NORMAL",
            #     "tradingsymbol": "SBIN-EQ",
            #     "symboltoken": "3045",
            #     "transactiontype": "BUY",
            #     "exchange": "NSE",
            #     "ordertype": "LIMIT",
            #     "producttype": "INTRADAY",
            #     "duration": "DAY",
            #     "price": "2",
            #     "squareoff": "0",
            #     "stoploss": "0",
            #     "quantity": "1"
            # }

            orderparams = {
                "variety": my_variety,
                "tradingsymbol": my_symbol,
                "symboltoken": my_token,
                "transactiontype": my_type,
                "exchange": my_exchange,
                "ordertype": my_order_type,
                "producttype": my_product_type,
                "duration": "DAY",
                "price": round(my_price,1),
                "squareoff": round(my_squar_off, 1),
                "stoploss": round(my_stop_loss, 1),
                "quantity": my_quantity,
                "tag": my_symbol,
                'ordertag': my_ordertag
            }
            # Method 1: Place an order and return the order ID
            # orderid = self.smartApi.placeOrder(orderparams)
            self.logger_obj.info('Order Details: {}'.format(orderparams))
            #orderid = self.smartApi.placeOrderFullResponse(orderparams)
            #self.logger_obj.info(f"Placed Order : {orderid}")

        except Exception as e:
            self.logger_obj.exception(f"Order placement failed: {e}")
