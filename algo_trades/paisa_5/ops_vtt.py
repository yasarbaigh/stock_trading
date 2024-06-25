import time

from common_utils.log_utils import LogUtils
from common_utils.redis_utils import RedisHelper
from paisa_5.p5_utils import clone_vtt_order, is_allowed_symbol, check_stop, export_to_json
from paisa_5.p5_values import VTT_WAIT, MIN_WAIT, WAIT_10_SEC
from paisa_5.p5_words import INITIAL_ORDER_STATUS, BUY_SELL, VTT_ORDER_ID, SYMBOL, \
    SCRIP_CODE, VTT_MODIFIED, INITIAL_STATUS, QUANTITY, INITIAL_TRIGGER_PRICE, MATCHING_CONDITION, \
    INITIAL_LIMIT_PRICE, BUY_NUM, VTT_ALLOWED_STATUS, ORDER_REJECTED_STATUS, CANCELLED, VTT_CANCEL, RDS_VTT_KEY, \
    ORDER_COMPLETED_STATUS, VTT_EXECUTED

logger_obj = LogUtils.return_logger(__name__)
from collections import OrderedDict

rds_clnt = RedisHelper()


def vtt_exists(ri_vtts, src_vtt_item):
    order_exists = False
    new_vtt = False
    modified_vtt = False
    for ele in ri_vtts:
        if ele.get(INITIAL_ORDER_STATUS) in ORDER_REJECTED_STATUS:
            continue
        elif ele.get(SCRIP_CODE) == src_vtt_item.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_vtt_item.get(BUY_SELL):
            order_exists = True
            if src_vtt_item.get(INITIAL_STATUS) == VTT_MODIFIED:
                if abs(float(src_vtt_item.get(INITIAL_LIMIT_PRICE)) - float(ele.get(
                        INITIAL_LIMIT_PRICE))) > .5:

                    modified_vtt = clone_vtt_order(src_vtt_item, True)
                    modified_vtt[VTT_ORDER_ID] = ele.get(VTT_ORDER_ID)
                    break
                elif src_vtt_item.get(INITIAL_TRIGGER_PRICE) != ele.get(INITIAL_TRIGGER_PRICE) or src_vtt_item.get(
                        MATCHING_CONDITION) != ele.get(MATCHING_CONDITION) or src_vtt_item.get(QUANTITY) != ele.get(
                    QUANTITY):
                    # prepare modified vtt,
                    modified_vtt = clone_vtt_order(src_vtt_item, True)
                    modified_vtt[VTT_ORDER_ID] = ele.get(VTT_ORDER_ID)
                    break
                else:
                    # modification already done.
                    break

            else:
                # current order is sufficient
                break

    if order_exists is False:
        new_vtt = clone_vtt_order(src_vtt_item)
    return new_vtt, modified_vtt


def cancel_vtt_if_exists(accsor, ri_vtts, src_vtt_item):
    for ele in ri_vtts:
        if ele.get(INITIAL_ORDER_STATUS) in ORDER_REJECTED_STATUS or ele.get(INITIAL_ORDER_STATUS) in ORDER_COMPLETED_STATUS:
            continue
        elif ele.get(SCRIP_CODE) == src_vtt_item.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_vtt_item.get(BUY_SELL):

            if ele.get(QUANTITY) == src_vtt_item.get(QUANTITY) or src_vtt_item.get(MATCHING_CONDITION):
                accsor.cancel_vtt(ele.get(VTT_ORDER_ID))
                return accsor.get_all_vtts()

    return ri_vtts


def copy_vtts(accsor):
    try:
        src_vtt_orders = rds_clnt.get_json(RDS_VTT_KEY)

        logger_obj.info('Source Vtts count : {}'.format(len(src_vtt_orders)))

        ri_vtt_orders = accsor.get_all_vtts()
        for item in src_vtt_orders:
            if item.get(INITIAL_ORDER_STATUS) in ORDER_REJECTED_STATUS or item.get(
                    INITIAL_ORDER_STATUS) in ORDER_COMPLETED_STATUS:
                ri_vtt_orders = cancel_vtt_if_exists(accsor, ri_vtt_orders, item)

            elif item.get(BUY_SELL) == BUY_NUM and item.get(
                    INITIAL_ORDER_STATUS) in VTT_ALLOWED_STATUS and is_allowed_symbol(
                item.get(SYMBOL)):
                create_vtt, modified_vtt = vtt_exists(ri_vtt_orders, item)
                if create_vtt:
                    accsor.place_vtt(create_vtt)
                    ri_vtt_orders = accsor.get_all_vtts()
                elif modified_vtt:
                    accsor.modify_vtt(modified_vtt)
                    ri_vtt_orders = accsor.get_all_vtts()
            else:
                logger_obj.info('skipped : {}'.format(item.get(SYMBOL)))

        logger_obj.info('Placed ALL Vtts.')
        prepare_vtt_diff(accsor)
        rds_clnt.set_json(RDS_VTT_KEY, [])
    except Exception as e:
        logger_obj.error(f"VTT_MODIFIED error : {e}")

    finally:
        check_stop(WAIT_10_SEC)


def prepare_vtt_diff(accsor):
    time.sleep(MIN_WAIT)

    od_src = OrderedDict()
    od_ri = OrderedDict()
    for item in rds_clnt.get_json(RDS_VTT_KEY):
        if item.get(INITIAL_ORDER_STATUS) not in ORDER_REJECTED_STATUS:
            od_src[item.get(SYMBOL)] = item

    for item in accsor.get_all_vtts():
        if item.get(INITIAL_ORDER_STATUS) not in ORDER_REJECTED_STATUS:
            od_ri[item.get(SYMBOL)] = item

    export_to_json('src.json', od_src.values())
    export_to_json('ri.json', od_ri.values())


def cancel_all_vtts(accsor):
    cnt = 0
    for ele in accsor.get_all_vtts():
        if ele.get(INITIAL_ORDER_STATUS) == CANCELLED and ele.get(INITIAL_STATUS) == VTT_CANCEL:
            continue
        else:
            # accsor.cancel_vtt(ele.get(VTT_ORDER_ID))
            logger_obj.info("Cancelling VTT: {}".format(ele.get(SYMBOL)))
            cnt += 1

    logger_obj.info('Cancelled Vtts count {}'.format(cnt))
