import time
from datetime import datetime

from pytz import timezone

from angel_one.angel_utils import should_place_order, prepare_option_name, check_stop
from angel_one.configs import TYPE_SELL, ANGEL_1_NSE, ANGEL_1_BSE
from angel_one.token_ids import MID_CP_NIFTY, NIFTY_50, FIN_NIFTY, INDEX_TOKEN_IDS, SENSEX
from common_utils.log_utils import LogUtils

continue_setup = True
logger_obj = LogUtils.return_logger(__name__)


def process_orders(ltp, token_key, token_v):
    dt_now = datetime.now(timezone("Asia/Kolkata"))
    if dt_now.hour == 9 and dt_now.minute < 20:
        check_first_step = True
    else:
        check_first_step = False

    check_second_step = True
    check_third_step = True
    return check_first_step, check_second_step, check_third_step


def check_and_place_order(conn, token_key, token_v, price):
    time.sleep(.5)  # adding delay
    if token_key == SENSEX:
        option_names = prepare_option_name(ANGEL_1_BSE, token_v.get('prefix'), price)
    else:
        option_names = prepare_option_name(ANGEL_1_NSE, token_v.get('prefix'), price)
        # option_names = [token_v.get('prefix').format(dt.strftime('%d%b%y'), price, 'CE').upper(),
        #             token_v.get('prefix').format(dt.strftime('%d%b%y'), price, 'PE').upper()]

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
                                    my_token=item.get('token'), my_type=TYPE_SELL, my_price=1,
                                    my_quantity=token_v.get('order_lots') * item.get('lotsize'))
            else:
                logger_obj.warn('Script {} not found.'.format(option_name))
        else:
            logger_obj.info('For option {} , order already exist.'.format(option_name))


def weekly_expiry_every_legs(conn, ):
    logger_obj.info('Starting weekly expiry legs Strategy.')

    while continue_setup:
        try:

            logger_obj.info('\n\n\n\nStarting an weekly_expiry_every_legs iteration: ')
            dt_now = datetime.now(timezone("Asia/Kolkata"))

            if dt_now.hour > 15:
                logger_obj.info('Market hour exceeded so stopping.')
                return

            if dt_now.isoweekday() == 1:  # MONDAY
                token_key = MID_CP_NIFTY
            elif dt_now.isoweekday() == 2:  # TUESDAY
                token_key = FIN_NIFTY
            elif dt_now.isoweekday() == 5:  # FRIDAY
                token_key = SENSEX
            else:
                token_key = NIFTY_50

            token_v = INDEX_TOKEN_IDS.get(token_key)

            ltp = conn.get_ltp(my_exchange=token_v.get('exchange'), my_token=token_v.get('symboltoken'))
            if ltp.get('errorcode'):
                logger_obj.error('Angel Error : {}'.format(ltp))
                continue

            check_first_step, check_second_step, check_third_step = process_orders(ltp, token_key, token_v)

            if check_first_step:
                open = round(ltp.get('data').get('open'))
                modulo_diff = open % token_v.get('option_step')
                check_low = open - modulo_diff
                check_high = open + (token_v.get('option_step') - modulo_diff)

                logger_obj.info(
                    'Comparing check-low {}   check-high {} , with ltp {}'.format(check_low, check_high,
                                                                                  ltp.get('data')))
                if ltp.get('data').get('low') < check_low:
                    check_and_place_order(conn, token_key, token_v, check_low)

                if ltp.get('data').get('high') > check_high:
                    check_and_place_order(conn, token_key, token_v, check_high)

            # first step process

            for step in ['second_step', 'third_step', 'fourth_step']:
                open = round(ltp.get('data').get('open'))
                modulo_diff = open % token_v.get('option_step')
                check_low = open - modulo_diff - token_v.get(step)
                check_high = open + (token_v.get('option_step') - modulo_diff) + token_v.get(step)

                logger_obj.info(
                    'Comparing check-low {}   check-high {} , with ltp {}'.format(check_low, check_high,
                                                                                  ltp.get('data')))
                if ltp.get('data').get('low') < check_low:
                    check_and_place_order(conn, token_key, token_v, check_low)

                if ltp.get('data').get('high') > check_high:
                    check_and_place_order(conn, token_key, token_v, check_high)


        except Exception as e:
            logger_obj.error("Errot in weekly_expiry_every_legs: {}".format(e))
        finally:
            check_stop()
