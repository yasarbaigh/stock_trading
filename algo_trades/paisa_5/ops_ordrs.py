import time
from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils
from common_utils.redis_utils import RedisHelper
from paisa_5.p5_utils import check_stop
from paisa_5.p5_values import MID_WAIT, MAX_PROFIT, WAIT_10_SEC, WAIT_35_SEC, P5_EXIT_PRICE
from paisa_5.p5_words import SCRIP_CODE, BUY_SELL, ORDER_ALLOWED_STATUS, ORDER_STATUS, ORDER_REJECTED_STATUS, \
    EXCH_ORDER_ID, ORDER_REQUESTER_CODE, ORDER_5PVTT, B, S, POSITION_NETQTY, EXCH, EXCH_TYPE, QTY, RATE, \
    RDS_ORDERS_KEY, ORDER_OPEN, POSITION_BUY_AVG_RATE, SL_TRIGGER_RATE, SCRIP_NAME
from jproperties import Properties

logger_obj = LogUtils.return_logger(__name__)
rds_clnt = RedisHelper()
configs = Properties()

def check_order_exists(accsor, ri_ordrs, src_order):
    for ele in ri_ordrs:
        if ele.get(SCRIP_CODE) == src_order.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_order.get(BUY_SELL):

            if src_order.get(ORDER_STATUS).strip() in ORDER_REJECTED_STATUS and ele.get(
                    ORDER_STATUS).strip() not in ORDER_REJECTED_STATUS:
                accsor.cancel_normal_order(ele.get(EXCH_ORDER_ID))
            if ele.get(ORDER_STATUS).strip() in ORDER_ALLOWED_STATUS:
                # modify

                # order exists
                pass

    # by this time, it should had modified-order
    # accsor.create_order(src_order)


def cancel_order(accsor, ri_ordrs, src_order):
    for ele in ri_ordrs:
        if ele.get(SCRIP_CODE) == src_order.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_order.get(BUY_SELL):
            if ele.get(ORDER_STATUS).strip() in ORDER_REJECTED_STATUS:
                pass
                # already cancelled
            else:
                accsor.cancel_normal_order(ele.get(EXCH_ORDER_ID))

            break


def copy_orders(accsor, ):
    try:
        time.sleep(MID_WAIT)
        src_orders = rds_clnt.get_json(RDS_ORDERS_KEY)

        logger_obj.info('Received Source Orders {}'.format(src_orders))
        ri_ordrs = accsor.get_all_orders()
        for item in src_orders:
            if item.get(ORDER_STATUS) in ORDER_REJECTED_STATUS:
                # cancel order
                check_order_exists(accsor, ri_ordrs, item)
            elif item.get(ORDER_REQUESTER_CODE) == ORDER_5PVTT:
                # vtt order , so leave it
                continue
            elif item.get(BUY_SELL) == B:

                # check orders if does not exist create
                check_order_exists(accsor, ri_ordrs, item)
                pass
            elif item.get(BUY_SELL) == S:
                # SELL ORDER, so skip it
                pass

        rds_clnt.set_json(RDS_ORDERS_KEY, [])

    except Exception as e:
        logger_obj.error(f"VTT_MODIFIED error : {e}")
    finally:
        check_stop(WAIT_10_SEC)


def place_sell_orders(accsor):
    postns = accsor.get_all_positions()
    ordrs = accsor.get_all_orders()

    for item in postns:
        place_close_order = False
        if item.get(POSITION_NETQTY) > 0:
            place_close_order = True
            for ord in ordrs:
                if (ord.get(SCRIP_CODE) == item.get(SCRIP_CODE) and ord.get(BUY_SELL) == S and
                        ord.get(ORDER_STATUS, '').strip() in ORDER_OPEN):
                    place_close_order = False

        if place_close_order:
            prepare_sell_order(accsor, item)


def prepare_sell_order(accsor, postn):
    with open(P5_EXIT_PRICE, 'rb') as config_file:
        configs.load(config_file)

    script_name = postn.get(SCRIP_NAME).split(' ')[0]
    if configs.get(script_name):
        sell_price = float(configs.get(script_name).data)
    else :
        sell_price = ((postn.get(POSITION_NETQTY) * postn.get(POSITION_BUY_AVG_RATE)) + MAX_PROFIT) / postn.get(
        POSITION_NETQTY)

    sell_ordr = {BUY_SELL: S, EXCH: postn.get(EXCH), EXCH_TYPE: postn.get(EXCH_TYPE), SCRIP_CODE: postn.get(SCRIP_CODE)
        , QTY: postn.get(POSITION_NETQTY), RATE: round(sell_price, 1), SL_TRIGGER_RATE: 0}

    accsor.create_order(sell_ordr)


def manage_orders(accsor):
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    if True:
        pass
        # ZZZ  delete after change, change below elif -> if

    elif dt_now.hour > 15:
        logger_obj.info('After market hours ')
        return
    elif (dt_now.hour >= 0 and dt_now.hour < 9) or (dt_now.hour == 9 and dt_now.minute < 15):
        market_yet_to_start = True
        while market_yet_to_start:
            time.sleep(WAIT_35_SEC)
            market_yet_to_start = False if dt_now.hour == 9 and dt_now.minute >= 15 else True
            accsor.get_all_orders()
            logger_obj.debug('Market yet to start')

    while True:  # ZZZ  dt_now.hour <= 15:
        if dt_now.hour >= 23 and dt_now.minute > 20:  # dt_now.hour >= 15 and dt_now.minute > 20:
            logger_obj.info('Market hour exceeded. So exiting BYE Bye!!!')
            break
        try:
            place_sell_orders(accsor)
            copy_orders(accsor)
            time.sleep(WAIT_10_SEC)
        except Exception as ex:
            logger_obj.error('Some error in manage_orders {}'.format(ex), ex)
