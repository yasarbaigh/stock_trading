import os
import time
from datetime import datetime, timedelta

from pytz import timezone

from angel_one.configs import ALLOWED_ORDER_STATUS, ANGEL_1_BSE, ANGEL_1_NSE, STOP_CHECK, STOPPED
from angel_one.token_ids import WAIT_TIME
from common_utils.log_utils import LogUtils

logger_obj = LogUtils.return_logger(__name__)


def should_place_order(script_name, orders):
    pass
    if orders.get('data') is not None:
        for item in orders.get('data', []):
            if item.get('tradingsymbol') == script_name and item.get('orderstatus') in ALLOWED_ORDER_STATUS:
                return False
    return True


def prepare_option_name(broker_exchange, prefix, price):
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    if dt_now.isoweekday() == 3:  # Wednesday
        dt_now = dt_now + timedelta(days=1)  # special case wednesday & thursday focus on nifty

    if ANGEL_1_NSE == broker_exchange:
        return [prefix.format(dt_now.strftime('%d%b%y'), price, 'CE').upper(),
                prefix.format(dt_now.strftime('%d%b%y'), price, 'PE').upper()]
    elif ANGEL_1_BSE == broker_exchange:
        # this below formatting works only in LINUX ,
        # SENSEX{}{}{}   TO SENSEX2441274100CE   (SENSEX 2024 APRIL 12 , 74100 ce)
        return [prefix.format(dt_now.strftime('%y%-m%d'), price, 'CE').upper(),
                prefix.format(dt_now.strftime('%y%-m%d'), price, 'PE').upper()]


def check_stop():
    if os.path.isfile(STOP_CHECK):
        logger_obj.info(f"Stop exist, so exiting : {STOP_CHECK}")
        os.rename(STOP_CHECK, STOPPED)
        exit(0)
    else:
        time.sleep(WAIT_TIME)
