import os
import time
from datetime import datetime, timedelta

from pytz import timezone

from angel_one.configs import ALLOWED_ORDER_STATUS, ANGEL_1_BSE, ANGEL_1_NSE, STOP_CHECK, STOPPED, TYPE_SELL, TYPE_BUY
from angel_one.token_ids import WAIT_TIME, SENSEX
from common_utils.log_utils import LogUtils

logger_obj = LogUtils.return_logger(__name__)


def should_place_order(script_name, orders, t_type):
    pass
    if orders.get('data') is not None:
        for item in orders.get('data', []):
            if item.get('tradingsymbol') == script_name and item.get(
                    'orderstatus') in ALLOWED_ORDER_STATUS and item.get('transactiontype') == t_type:
                return False
    return True


def prepare_option_name(broker_exchange, prefix, price, date_part=None, previous_initiate=False, option_step=0):
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    if previous_initiate:
        if dt_now.isoweekday() == 5:  # Friday
            dt_now = dt_now + timedelta(days=3)  # if friday, choosing monday
        else:
            dt_now = dt_now + timedelta(days=1)  # else next day

    # fri,mon - midcpnifty, tuesday-finnifty , wednes,thrus-nifty50
    if dt_now.isoweekday() == 3:  # if Wednesday; choosing to thursday for nifty expiry
        dt_now = dt_now + timedelta(days=1)
    elif dt_now.isoweekday() == 5:  # FRIDAY
        dt_now = dt_now + timedelta(days=3)  # if friday, choosing monday for midcp-expiry

        # for current-day options
    if ANGEL_1_NSE == broker_exchange:
        date_part = date_part if date_part else dt_now.strftime('%d%b%y')

        regular_options = [prefix.format(date_part, price, 'CE').upper(),
                           prefix.format(date_part, price, 'PE').upper()]
        # adding other side hedges
        otm3_options = [prefix.format(date_part, price + (3 * option_step), 'CE').upper(),
                        prefix.format(date_part, price - (3 * option_step), 'PE').upper()]
        return regular_options, otm3_options

    elif ANGEL_1_BSE == broker_exchange:
        # this below formatting works only in LINUX ,
        # SENSEX{}{}{}   TO SENSEX2441274100CE   (SENSEX 2024 APRIL 12 , 74100 ce)
        date_part = date_part if date_part else dt_now.strftime('%y%-m%d')
        regular_options = [prefix.format(date_part, price, 'CE').upper(),
                           prefix.format(date_part, price, 'PE').upper()]

        # adding other side hedges
        otm3_options = [prefix.format(date_part, price + (3 * option_step), 'CE').upper(),
                        prefix.format(date_part, price - (3 * option_step), 'PE').upper()]
        return regular_options, otm3_options


def prepare_option_name_with_diff(broker_exchange, prefix, price, diff, previous_initiate=False):
    '''
    Especially used for previous_initiate order
    :param broker_exchange:
    :param prefix:
    :param price:
    :param diff:
    :param previous_initiate:
    :return:
    '''
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    if previous_initiate:
        if dt_now.isoweekday() == 5:  # Friday
            dt_now = dt_now + timedelta(days=3)  # if friday, choosing monday
        else:
            dt_now = dt_now + timedelta(days=1)  # else next day

    # for current-day options
    if ANGEL_1_NSE == broker_exchange:
        return [prefix.format(dt_now.strftime('%d%b%y'), price, 'CE').upper(),
                prefix.format(dt_now.strftime('%d%b%y'), price - diff, 'PE').upper()]
    elif ANGEL_1_BSE == broker_exchange:
        # this below formatting works only in LINUX ,
        # SENSEX{}{}{}   TO SENSEX2441274100CE   (SENSEX 2024 APRIL 12 , 74100 ce)
        return [prefix.format(dt_now.strftime('%y%-m%d'), price, 'CE').upper(),
                prefix.format(dt_now.strftime('%y%-m%d'), price - diff, 'PE').upper()]


def check_stop():
    if os.path.isfile(STOP_CHECK):
        logger_obj.info(f"Stop exist, so exiting : {STOP_CHECK}")
        os.rename(STOP_CHECK, STOPPED)
        exit(0)
    else:
        time.sleep(WAIT_TIME)


def check_and_place_order(conn, token_key, token_v, price, my_order_tag, date_part=None, previous_initiate=False):
    time.sleep(.5)  # adding delay
    if token_key == SENSEX:
        option_names, otm3_options = prepare_option_name(ANGEL_1_BSE, token_v.get('prefix'), price, date_part,
                                                         previous_initiate,
                                                         token_v.get('option_step'))
    else:
        option_names, otm3_options = prepare_option_name(ANGEL_1_NSE, token_v.get('prefix'), price, date_part,
                                                         previous_initiate,
                                                         token_v.get('option_step'))

    orders = conn.get_orders()

    for option_name in option_names:
        logger_obj.info('Checking for option {} {}'.format(TYPE_SELL, option_name))
        time.sleep(.5)  # adding after each cycle
        if should_place_order(option_name, orders, TYPE_SELL):
            # script_name = 'NIFTY10APR2422450CE'
            # script_name = 'SENSEX2441274100CE'
            item = conn.get_script_details(option_name)
            if item:
                logger_obj.info('placing order of {}'.format(option_name))
                option_ltp = conn.get_ltp(my_exchange=item.get('exch_seg'), my_token=item.get('token'))
                if option_ltp.get('data') and option_ltp.get('data').get('ltp'):
                    logger_obj.info('Placing market-order at price: {}'.format(option_ltp.get('data').get('ltp')))

                # market orders price should be ZERO-0
                conn.order_placment(my_exchange=item.get('exch_seg'), my_symbol=item.get('symbol'),
                                    my_token=item.get('token'), my_type=TYPE_SELL, my_price=0,
                                    my_quantity=token_v.get('order_lots') * item.get('lotsize'),
                                    my_ordertag=my_order_tag)
            else:
                logger_obj.warn('Script {} not found.'.format(option_name))
        else:
            logger_obj.info('For option {} {}, order already exist.'.format(TYPE_SELL, option_name))

    orders = conn.get_orders()

    for buy_option_name in otm3_options:
        logger_obj.info('Checking for option {} {}'.format(TYPE_BUY, buy_option_name))
        time.sleep(.5)  # adding after each cycle
        if should_place_order(buy_option_name, orders, TYPE_BUY):
            # script_name = 'NIFTY10APR2422450CE'
            # script_name = 'SENSEX2441274100CE'
            item = conn.get_script_details(buy_option_name)
            if item:
                logger_obj.info('placing order of {}'.format(buy_option_name))
                option_ltp = conn.get_ltp(my_exchange=item.get('exch_seg'), my_token=item.get('token'))
                if option_ltp.get('data') and option_ltp.get('data').get('ltp'):
                    logger_obj.info('Placing market-order at price: {}'.format(option_ltp.get('data').get('ltp')))

                # market orders price should be ZERO-0
                conn.order_placment(my_exchange=item.get('exch_seg'), my_symbol=item.get('symbol'),
                                    my_token=item.get('token'), my_type=TYPE_BUY, my_price=0,
                                    my_quantity=token_v.get('order_lots') * item.get('lotsize'),
                                    my_ordertag=my_order_tag)
            else:
                logger_obj.warn('Script {} not found.'.format(buy_option_name))
        else:
            logger_obj.info('For option {} {} , order already exist.'.format(TYPE_BUY, buy_option_name))


def check_and_place_order_with_diff(conn, token_key, token_v, price, my_order_tag, previous_initiate=False):
    time.sleep(.5)  # adding delay
    diff = 2 * token_v.get('option_step')
    if token_key == SENSEX:
        option_names = prepare_option_name_with_diff(ANGEL_1_BSE, token_v.get('prefix'), price, diff, previous_initiate)
    else:
        option_names = prepare_option_name_with_diff(ANGEL_1_NSE, token_v.get('prefix'), price, diff, previous_initiate)

    orders = conn.get_orders()

    for option_name in option_names:
        logger_obj.info('Checking for option {}'.format(option_name))
        time.sleep(.5)  # adding after each cycle
        if should_place_order(option_name, orders):
            # script_name = 'NIFTY10APR2422450CE'
            # script_name = 'SENSEX2441274100CE'
            item = conn.get_script_details(option_name)
            if item:
                logger_obj.info('placing order of {}'.format(option_name))
                option_ltp = conn.get_ltp(my_exchange=item.get('exch_seg'), my_token=item.get('token'))
                if option_ltp.get('data') and option_ltp.get('data').get('ltp'):
                    logger_obj.info('Placing market-order at price: {}'.format(option_ltp.get('data').get('ltp')))

                conn.order_placment(my_exchange=item.get('exch_seg'), my_symbol=item.get('symbol'),
                                    my_token=item.get('token'), my_type=TYPE_SELL, my_price=0,
                                    my_quantity=token_v.get('order_lots') * item.get('lotsize'),
                                    my_ordertag=my_order_tag)
            else:
                logger_obj.warn('Script {} not found.'.format(option_name))
        else:
            logger_obj.info('For option {} , order already exist.'.format(option_name))


def compute_first_order_price(conn, token_v, ltp, tag_prefix):
    time.sleep(.5)
    orders = conn.get_orders()
    first_order_price = 0
    if orders.get('data'):
        for item in orders.get('data', []):
            if item.get('ordertag') and item.get('ordertag').startswith(tag_prefix):
                first_order_price = int(item.get('ordertag').replace(tag_prefix, ''))
                return first_order_price

    if first_order_price == 0:
        first_order_price = round(ltp.get('data').get('open'))
        modulo_diff = first_order_price % token_v.get('option_step')
        first_order_price = first_order_price + (token_v.get('option_step') - modulo_diff)

    return first_order_price
