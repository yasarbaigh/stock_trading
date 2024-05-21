import time
from datetime import datetime

from pytz import timezone

from angel_one.angel_utils import check_stop, check_and_place_order, compute_first_order_price
from angel_one.configs import STRATEGY_1_RANGA_ORDER_2, STRATEGY_1_RANGA_ORDER_1, STRATEGY_1_RANGA_ORDER_1_PREFIX
from angel_one.token_ids import MID_CP_NIFTY, NIFTY_50, FIN_NIFTY, INDEX_TOKEN_IDS
from common_utils.log_utils import LogUtils

continue_setup = True
logger_objt = LogUtils.return_logger(__name__)


def process_orders(ltp, token_key, token_v):
    dt_now = datetime.now(timezone("Asia/Kolkata"))
    if dt_now.hour == 9 and dt_now.minute < 20:
        check_first_step = True
    else:
        check_first_step = False

    check_second_step = True
    return check_first_step, check_second_step


def ranga_weekly_expiry_every_legs_1(conn, adhoc_token_key=None, adhoc_date_part=None):
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    if adhoc_date_part:
        token_key = adhoc_token_key  # adhoc-custome-index
    else:
        if dt_now.isoweekday() == 1:  # MONDAY
            token_key = MID_CP_NIFTY
        elif dt_now.isoweekday() == 2:  # TUESDAY
            token_key = FIN_NIFTY
        elif dt_now.isoweekday() == 3:  # Wednesday
            token_key = NIFTY_50
        elif dt_now.isoweekday() == 4:  # Thursday
            token_key = NIFTY_50
        elif dt_now.isoweekday() == 5:  # FRIDAY
            token_key = MID_CP_NIFTY
        else:
            token_key = NIFTY_50

    # logger_objt.info('Starting weekly expiry legs Strategy.')

    token_v = INDEX_TOKEN_IDS.get(token_key)

    need_to_place_first_order = True
    first_order_price = 0

    while continue_setup:
        try:

            logger_objt.info('\n\n\n\nStarting an ranga_weekly_expiry_every_legs iteration: ')
            dt_now = datetime.now(timezone("Asia/Kolkata"))

            if dt_now.hour >= 15 or dt_now.hour < 9:
                time.sleep(100)
                logger_objt.info('Market hour exceeded so stopping.')
                return

            ltp = conn.get_ltp(my_exchange=token_v.get('exchange'), my_token=token_v.get('symboltoken'))
            if ltp.get('errorcode'):
                logger_objt.error('Angel Error : {}'.format(ltp))
                continue

            check_first_step, check_second_step = process_orders(ltp, token_key, token_v)

            if check_first_step:
                open = round(ltp.get('data').get('open'))
                modulo_diff = open % token_v.get('option_step')
                check_low = open - modulo_diff
                check_high = open + (token_v.get('option_step') - modulo_diff)

                logger_objt.info(
                    'Comparing check-low {}  check-high {} , with ltp {}'.format(check_low, check_high,
                                                                                 ltp.get('data')))
                if need_to_place_first_order and ltp.get('data').get('high') > check_high:
                    check_and_place_order(conn, token_key, token_v, check_high,
                                          STRATEGY_1_RANGA_ORDER_1.format(check_high), adhoc_date_part)
                    first_order_price = check_high
                    need_to_place_first_order = False

                if need_to_place_first_order and ltp.get('data').get('low') < check_low:
                    check_and_place_order(conn, token_key, token_v, check_low,
                                          STRATEGY_1_RANGA_ORDER_1.format(check_low), adhoc_date_part)
                    first_order_price = check_low
                    need_to_place_first_order = False
            elif need_to_place_first_order and first_order_price == 0:
                first_order_price = compute_first_order_price(conn, token_v, ltp, STRATEGY_1_RANGA_ORDER_1_PREFIX)
                need_to_place_first_order = False

            # first step process
            logger_objt.info('First Order price is {}'.format(first_order_price))
            if need_to_place_first_order is False:

                for step in ['second_step', 'third_step', 'fourth_step']:

                    check_low = first_order_price - token_v.get(step)
                    check_high = first_order_price + token_v.get(step)

                    logger_objt.info(
                        'Comparing check-low {}   check-high {} , with ltp {}'.format(check_low, check_high,
                                                                                      ltp.get('data')))
                    if ltp.get('data').get('low') < check_low:
                        check_and_place_order(conn, token_key, token_v, check_low, STRATEGY_1_RANGA_ORDER_2,
                                              adhoc_date_part)

                    if ltp.get('data').get('high') > check_high:
                        check_and_place_order(conn, token_key, token_v, check_high, STRATEGY_1_RANGA_ORDER_2,
                                              adhoc_date_part)


        except Exception as e:
            logger_objt.error("Error in weekly_expiry_every_legs: {}".format(e))
        finally:
            check_stop()
