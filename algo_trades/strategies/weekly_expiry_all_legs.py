from datetime import datetime

from pytz import timezone

from angel_one.angel_utils import check_stop, check_and_place_order
from angel_one.configs import STRATEGY_1_EXPIRY_LEG
from angel_one.token_ids import MID_CP_NIFTY, NIFTY_50, FIN_NIFTY, INDEX_TOKEN_IDS, SENSEX, BANK_NIFTY
from common_utils.log_utils import LogUtils
from strategies.previous_day_initiator import previous_day_intiate

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


def weekly_expiry_every_legs(conn, ):
    logger_obj.info('Starting weekly expiry legs Strategy.')

    while continue_setup:
        try:

            logger_obj.info('\n\n\n\nStarting an weekly_expiry_every_legs iteration: ')
            dt_now = datetime.now(timezone("Asia/Kolkata"))

            if dt_now.hour > 15 or dt_now.hour < 9:
                logger_obj.info('Market hour exceeded so stopping.')
                return

            if dt_now.isoweekday() == 1:  # MONDAY
                token_key = MID_CP_NIFTY
            elif dt_now.isoweekday() == 2:  # TUESDAY
                token_key = FIN_NIFTY
            elif dt_now.isoweekday() == 3:  # Wednesday
                token_key = NIFTY_50
            elif dt_now.isoweekday() == 5:  # FRIDAY
                token_key = MID_CP_NIFTY  # SENSEX
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
                    check_and_place_order(conn, token_key, token_v, check_low, STRATEGY_1_EXPIRY_LEG)

                if ltp.get('data').get('high') > check_high:
                    check_and_place_order(conn, token_key, token_v, check_high, STRATEGY_1_EXPIRY_LEG)

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
                    check_and_place_order(conn, token_key, token_v, check_low, STRATEGY_1_EXPIRY_LEG)

                if ltp.get('data').get('high') > check_high:
                    check_and_place_order(conn, token_key, token_v, check_high, STRATEGY_1_EXPIRY_LEG)


        except Exception as e:
            logger_obj.error("Errot in weekly_expiry_every_legs: {}".format(e))
        finally:
            exit_orders(conn, dt_now)
            check_stop()


def exit_orders(conn, dt_now):
    if dt_now.hour == 15 and dt_now.minute == 15:
        try:
            orders = conn.get_orders()
            if orders.get('data') is not None:
                for item in orders.get('data', []):
                    ltp = conn.get_ltp(my_exchange=item.get('exchange'), my_token=item.get('symboltoken'))
                    logger_obj.info(
                        f"\t\t\tExit price of placing script: {item.get('tradingsymbol')} \t {ltp.get('data', {}).get('ltp')}")
        except Exception as e:
            logger_obj.error("Error in exit_orders: {}".format(e))
        finally:
            previous_day_intiate(conn)
    else:
        return False

