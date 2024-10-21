import time
from datetime import datetime

from angel_one.configs import BASE_PREFIX, SEGMENT_NSE_FNO, TYPE_BUY, VARIETY_BRACKET_ORDER, ORDER_LIMIT, \
    PRODCUT_TYPE_BRACKET_ORDER, INTERVAL_5_MIN, INTERVAL_15_MIN, INTERVAL_10_MIN
from common_utils.log_utils import LogUtils

LogUtils(BASE_PREFIX + "/opt/tmp/angel_1/angel_api_{}.log")

from angel_one.angel_utils import should_place_order

from FLASK_CONFIGS import ACTION_START, ACTION, SELECTED_STOCK, THREAD_KEY, SELECTED_STRIKE, SELECTED_OPTIONS, \
    OPTION_BOTH, OPTION_CE, SELECTED_DATE, SELECTED_TF, SELECTED_LOT, OPTION_PE, PUNCHED_AT, REASON, ACTION_STOP, \
    PLACE_PE_ORDER, PLACE_CE_ORDER, STRATEGY, CHOOSE_STRIKE
from angel_one.token_ids import INDEX_TOKEN_IDS
from common_utils.log_utils import LogUtils
from math_modals.math_conversion import candle_to_heikin_ashi

logger_objt = LogUtils.return_logger(__name__)
import pandas as pd

HEIKIN_TARGET_POINT = 20


def hekin_aashi_in_index_strikes(conn, thread_args):
    try:

        token_key = thread_args.get(SELECTED_STOCK)
        token_v = INDEX_TOKEN_IDS.get(token_key)

        thread_args[PLACE_CE_ORDER] = True
        thread_args[PLACE_PE_ORDER] = True
        thread_args[REASON] = ''
        thread_args[CHOOSE_STRIKE] = ''

        ltp = conn.get_ltp(my_exchange=token_v.get('exchange'), my_token=token_v.get('symboltoken'))
        while ltp.get('errorcode'):
            logger_objt.error('Angel Error : {}'.format(ltp))
            time.sleep(10)
            continue

        open = round(ltp.get('data').get('ltp'))
        modulo_diff = open % token_v.get('option_step')
        ltp_rounded = open + (token_v.get('option_step') - modulo_diff)

        logger_objt.info('Choosen ltp {} for combo {}'.format(ltp_rounded, thread_args.get(THREAD_KEY)))
        date_objt = datetime.strptime(thread_args.get(SELECTED_DATE), "%Y-%m-%d").date()

        pe_details = ce_details = None
        if thread_args.get(SELECTED_OPTIONS) == OPTION_BOTH or thread_args.get(SELECTED_OPTIONS) == OPTION_CE:
            ce_strike = ltp_rounded + (int(thread_args.get(SELECTED_STRIKE)) * token_v.get('option_step'))
            ce_option_name = token_v.get('prefix').format(date_objt.strftime('%d%b%y'), ce_strike, 'CE').upper()
            ce_details = conn.get_script_details(ce_option_name)
            thread_args[CHOOSE_STRIKE] += (str(ce_strike) + 'CE').upper()

        if thread_args.get(SELECTED_OPTIONS) == OPTION_BOTH or thread_args.get(SELECTED_OPTIONS) == OPTION_PE:
            pe_strike = ltp_rounded - (int(thread_args.get(SELECTED_STRIKE)) * token_v.get('option_step'))
            pe_option_name = token_v.get('prefix').format(date_objt.strftime('%d%b%y'), pe_strike, 'PE').upper()
            pe_details = conn.get_script_details(pe_option_name)
            thread_args[CHOOSE_STRIKE] += (str(ce_strike) + 'PE').upper()

        logger_objt.info('Chosen ce_details {} '.format(ce_details))
        logger_objt.info('Chosen pe_details {} '.format(pe_details))

        if pe_details is None and ce_details is None:
            thread_args[REASON] += '; No CE/PE Details , so exiting BYE BYE'
            logger_objt.info('No CE/PE Details , so exiting the thread. BYE BYE')
            thread_args.get(ACTION) == ACTION_STOP
            return

        # waiting for next-candle
        while thread_args.get(ACTION) == ACTION_START:
            dt = datetime.now()
            if thread_args.get(SELECTED_TF) == INTERVAL_5_MIN and dt.minute % 5 == 0:
                logger_objt.info('{} next candle matched. '.format(thread_args.get(THREAD_KEY)))
                time.sleep(35)
                break
            elif thread_args.get(SELECTED_TF) == INTERVAL_10_MIN and dt.minute % 10 == 0:
                logger_objt.info('{} next candle matched. '.format(thread_args.get(THREAD_KEY)))
                time.sleep(35)
                break
            elif thread_args.get(SELECTED_TF) == INTERVAL_15_MIN and dt.minute % 15 == 0:
                logger_objt.info('{} next candle matched. '.format(thread_args.get(THREAD_KEY)))
                time.sleep(35)
                break
            else:
                logger_objt.info(
                    'For {} waiting for next set of seconds & candle . '.format(thread_args.get(THREAD_KEY)))
                time.sleep(35)

        while thread_args.get(ACTION) == ACTION_START:
            place_attempt_iterate_skipped = True

            if ce_details and thread_args.get(PLACE_CE_ORDER):
                place_attempt_iterate_skipped = False
                process_option_HA(conn, thread_args, ce_details, PLACE_CE_ORDER)

            if pe_details and thread_args.get(PLACE_PE_ORDER):
                place_attempt_iterate_skipped = False
                process_option_HA(conn, thread_args, pe_details, PLACE_PE_ORDER)

            if place_attempt_iterate_skipped :
                logger_objt.info('Requested {} options placed, so breaking loop.'.format(thread_args.get(SELECTED_OPTIONS)))
                break
            else:
                time.sleep(20)

    except Exception as e:
        logger_objt.error('error hekin_ashi_in_index_strikes {}'.format(e))
        thread_args[REASON] += '; {}'.format(e)
    finally:
        pass


def process_option_HA(conn, thread_args, option_details, option_key):
    logger_objt.info('Checking for combo {}'.format(thread_args.get(THREAD_KEY)))
    candle_data = conn.get_candlde_data(SEGMENT_NSE_FNO, option_details.get('token'),
                                        thread_args.get(SELECTED_TF))

    df = pd.DataFrame(candle_data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    df['Date'] = pd.to_datetime(df['Date'])
    heikin_df = candle_to_heikin_ashi(df)
    if df.shape[0] < 2:
        logger_objt.info('skipping sufficient TF not available. {}'.format(df.shape))
        return
    last_value = heikin_df['HA_High'].iloc[-1]
    second_last_value = heikin_df['HA_High'].iloc[-2]

    if last_value > second_last_value:
        orders = conn.get_orders()
        if should_place_order(option_details.get('symbol'), orders, TYPE_BUY):
            logger_objt.info(
                'placing_order of {} at {} '.format(option_details.get('symbol'), heikin_df['HA_Close'].iloc[-1]))

            logger_objt.info("Last Row : {}".format(heikin_df.iloc[-1]))
            logger_objt.info("2nd-Last Row : {}".format(heikin_df.iloc[-2]))

            conn.order_placment(my_exchange=option_details.get('exch_seg'), my_symbol=option_details.get('symbol'),
                                my_token=option_details.get('token'), my_type=TYPE_BUY,
                                my_order_type=ORDER_LIMIT,
                                my_price=heikin_df['HA_Close'].iloc[-2],
                                my_stop_loss=heikin_df['HA_Low'].iloc[-2] - 2,
                                my_squar_off=HEIKIN_TARGET_POINT,
                                my_quantity=int(thread_args.get(SELECTED_LOT)) * option_details.get('lotsize'),
                                my_ordertag=thread_args.get(THREAD_KEY) + thread_args.get(PUNCHED_AT),
                                my_variety=VARIETY_BRACKET_ORDER,
                                my_product_type=PRODCUT_TYPE_BRACKET_ORDER)
            thread_args[option_key] = False
            thread_args[REASON] += '; {} Done at {}. '.format(option_key, datetime.now().strftime("%H:%M:%S"))

        else:
            logger_objt.info('for {} order-exists already, so Skipping.'.format(option_details))

# from angel_one.angel_connector import AngelConnector
#
# conn = AngelConnector()
# conn.generate_smart_api_session()
# conn.get_orders()
#
# pass
# start_args = {}
#
# start_args[SELECTED_STOCK] = 'NIFTY_50'
# start_args[SELECTED_TF] = 'FIVE_MINUTE'
# start_args[SELECTED_STRIKE] = '1'
# start_args[SELECTED_LOT] = '1'
# start_args[SELECTED_OPTIONS] = 'BOTH'
# start_args[ACTION] = ACTION_START
# start_args[STRATEGY] = 'HEIKIN_ASHI'
# start_args[SELECTED_DATE] = '2024-10-17'
# start_args[THREAD_KEY] = start_args[STRATEGY] + '_' + start_args.get(SELECTED_STOCK) + '_' + start_args[
#             SELECTED_DATE] + '_' + start_args.get(SELECTED_TF) + \
#                      '_' + start_args.get(SELECTED_STRIKE) + '_' + start_args[SELECTED_OPTIONS] + '_' + start_args.get(
#             SELECTED_LOT)
#
# hekin_aashi_in_index_strikes(conn, start_args)
