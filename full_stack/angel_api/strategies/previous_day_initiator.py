import time
from datetime import datetime

from pytz import timezone

from angel_one.angel_utils import check_stop, check_and_place_order, check_and_place_order_with_diff
from angel_one.configs import STRATEGY_2_PREVIOUS_INITIATED
from angel_one.token_ids import MID_CP_NIFTY, NIFTY_50, FIN_NIFTY, INDEX_TOKEN_IDS, SENSEX, BANK_NIFTY, WAIT_TIME
from common_utils.log_utils import LogUtils

continue_setup = True
logger_obj = LogUtils.return_logger(__name__)


def previous_day_intiate(conn):
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    if dt_now.isoweekday() == 1:  # MONDAY
        token_key = FIN_NIFTY
    elif dt_now.isoweekday() == 2:  # TUESDAY
        token_key = NIFTY_50
    elif dt_now.isoweekday() == 3:  # Wednesday
        token_key = NIFTY_50
    elif dt_now.isoweekday() == 4:  # Thursday
        token_key = MID_CP_NIFTY
    elif dt_now.isoweekday() == 5:  # FRIDAY
        token_key = MID_CP_NIFTY
    else:
        token_key = NIFTY_50

    token_v = INDEX_TOKEN_IDS.get(token_key)

    flag_continue = True

    previous_initiate_low = previous_initiate_high = 0
    while flag_continue:
        try:
            ltp = conn.get_ltp(my_exchange=token_v.get('exchange'), my_token=token_v.get('symboltoken'))
            if ltp.get('errorcode'):
                logger_obj.error('Angel Error : {}'.format(ltp))
                time.sleep(WAIT_TIME)
                continue
            else:
                this_price = round(ltp.get('data').get('ltp'))
                modulo_diff = this_price % token_v.get('option_step')
                previous_initiate_low = this_price - modulo_diff
                previous_initiate_high = this_price + (token_v.get('option_step') - modulo_diff)
                flag_continue = False
        except Exception as e:
            logger_obj.error("Errot in previous_day_intiate: {}".format(e))

    flag_continue = True
    while flag_continue:
        try:
            ltp = conn.get_ltp(my_exchange=token_v.get('exchange'), my_token=token_v.get('symboltoken'))
            if ltp.get('errorcode'):
                logger_obj.error('Angel Error in previous_day_intiate : {}'.format(ltp))
                time.sleep(WAIT_TIME)
                continue
            else:
                if previous_initiate_low > ltp.get('data').get('ltp'):

                    check_and_place_order(conn, token_key, token_v, previous_initiate_low,
                                          STRATEGY_2_PREVIOUS_INITIATED, previous_initiate=True)
                    check_and_place_order_with_diff(conn, token_key, token_v,
                                                    previous_initiate_low + token_v.get('option_step'),
                                                    'API_RANGA_2_', previous_initiate=True)
                    flag_continue = False
                elif previous_initiate_high < ltp.get('data').get('ltp'):

                    check_and_place_order(conn, token_key, token_v, previous_initiate_high,
                                          STRATEGY_2_PREVIOUS_INITIATED, previous_initiate=True)
                    check_and_place_order_with_diff(conn, token_key, token_v,
                                                    previous_initiate_high + token_v.get('option_step'),
                                                    STRATEGY_2_PREVIOUS_INITIATED, previous_initiate=True)
                    flag_continue = False
                else:
                    flag_continue = True
        except Exception as e:
            logger_obj.error("Erro in weekly_expiry_every_legs: {}".format(e))
        finally:
            check_stop()
            exit(0)
