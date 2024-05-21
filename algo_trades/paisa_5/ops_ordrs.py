import time

from common_utils.log_utils import LogUtils
from paisa_5.p5_utils import check_stop
from paisa_5.p5_values import MID_WAIT, VTT_WAIT
from paisa_5.p5_words import SCRIP_CODE, BUY_SELL, ORDER_ALLOWED_STATUS, ORDER_STATUS, ORDER_REJECTED_STATUS, \
    EXCH_ORDER_ID, ORDER_REQUESTER_CODE, ORDER_5PVTT, B, S

logger_obj = LogUtils.return_logger(__name__)


def check_order_exists(accsor, ri_ordrs, src_order):
    for ele in ri_ordrs:
        if ele.get(SCRIP_CODE) == src_order.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_order.get(BUY_SELL):

            if ele.get(ORDER_STATUS).strip() in ORDER_ALLOWED_STATUS:
                # modify

                # order exists
                pass

    # by this time, it should had modified-order
    accsor.create_order(src_order)


def cancel_order(accsor, ri_ordrs, src_order):
    for ele in ri_ordrs:
        if ele.get(SCRIP_CODE) == src_order.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_order.get(BUY_SELL):
            if ele.get(ORDER_STATUS).strip() in ORDER_REJECTED_STATUS:
                pass
                # already cancelled
            else:
                accsor.cancel_order(ele.get(EXCH_ORDER_ID))

            break


def copy_orders(accsor, amin_client, ri_client):
    try:
        time.sleep(MID_WAIT)
        amin_ordrs = amin_client.order_book()

        time.sleep(MID_WAIT)
        ri_ordrs = ri_client.order_book()
        for item in amin_ordrs:
            if item.get(ORDER_REQUESTER_CODE) == ORDER_5PVTT:

                # vtt order or rejected order so skip

                continue
            elif item.get(ORDER_STATUS) in ORDER_REJECTED_STATUS:
                # cancel order
                pass
            elif item.get(BUY_SELL) == B:

                # check orders if does not exist create
                check_order_exists(accsor, ri_ordrs, item)
                pass
            elif item.get(BUY_SELL) == S:
                # SELL ORDER
                # PASS check positions
                pass

    except Exception as e:
        logger_obj.error(f"VTT_MODIFIED error : {e}")
    finally:
        check_stop(VTT_WAIT)
