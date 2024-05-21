from common_utils.log_utils import LogUtils
from paisa_5.p5_utils import clone_vtt_order, is_allowed_symbol, check_stop
from paisa_5.p5_values import VTT_WAIT
from paisa_5.p5_words import VTT_ORDERS, INITIAL_ORDER_STATUS, VTT_ORDER_DATA, BUY_SELL, VTT_ORDER_ID, SYMBOL, \
    SCRIP_CODE, VTT_MODIFIED, INITIAL_STATUS, QUANTITY, INITIAL_TRIGGER_PRICE, MATCHING_CONDITION, \
    INITIAL_LIMIT_PRICE, BUY_NUM, VTT_ALLOWED_STATUS, ORDER_REJECTED_STATUS

logger_obj = LogUtils.return_logger(__name__)


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
                if src_vtt_item.get(INITIAL_TRIGGER_PRICE) != ele.get(INITIAL_TRIGGER_PRICE) or src_vtt_item.get(
                        MATCHING_CONDITION) != ele.get(MATCHING_CONDITION) or src_vtt_item.get(
                    QUANTITY) != ele.get(QUANTITY) or src_vtt_item.get(INITIAL_LIMIT_PRICE) != ele.get(
                    INITIAL_LIMIT_PRICE):
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


def cancel_vtt_if_exists(accsor, ri_vtts, src_vtt_item, ri_client):
    for ele in ri_vtts:
        if ele.get(INITIAL_ORDER_STATUS) in ORDER_REJECTED_STATUS:
            continue
        elif ele.get(SCRIP_CODE) == src_vtt_item.get(SCRIP_CODE) and ele.get(BUY_SELL) == src_vtt_item.get(BUY_SELL):

            if src_vtt_item.get(INITIAL_LIMIT_PRICE) == ele.get(INITIAL_LIMIT_PRICE) and ele.get(
                    QUANTITY) == src_vtt_item.get(QUANTITY):

                accsor.cancel_vtt(ele.get(VTT_ORDER_ID))
                return ri_client.vtt_order(VTT_ORDERS).get(VTT_ORDER_DATA)

    return ri_vtts


def copy_vtts(accsor, amin_client, ri_client):
    continue_vtt_check = True
    while continue_vtt_check:
        try:
            amin_vtt_orders = amin_client.vtt_order(VTT_ORDERS)

            logger_obj.info('Amin Vtt count : {}'.format(len(amin_vtt_orders.get(VTT_ORDER_DATA))))
            ri_vtt_orders = ri_client.vtt_order(VTT_ORDERS).get(VTT_ORDER_DATA)
            for item in amin_vtt_orders.get(VTT_ORDER_DATA, []):
                if item.get(INITIAL_ORDER_STATUS) in ORDER_REJECTED_STATUS:
                    ri_vtt_orders = cancel_vtt_if_exists(accsor, ri_vtt_orders, item, ri_client)

                elif item.get(BUY_SELL) == BUY_NUM and item.get(
                        INITIAL_ORDER_STATUS) in VTT_ALLOWED_STATUS and is_allowed_symbol(
                    item.get(SYMBOL)):
                    create_vtt, modified_vtt = vtt_exists(ri_vtt_orders, item)
                    if create_vtt:
                        accsor.place_vtt(create_vtt)
                        ri_vtt_orders = ri_client.vtt_order(VTT_ORDERS).get(VTT_ORDER_DATA)
                    elif modified_vtt:
                        accsor.modify_vtt(modified_vtt)
                        ri_vtt_orders = ri_client.vtt_order(VTT_ORDERS).get(VTT_ORDER_DATA)
                else:
                    logger_obj.info('skipped : {}'.format(item.get(SYMBOL)))

            logger_obj.info('Placed ALL Vtts.')

        except Exception as e:
            logger_obj.error(f"VTT_MODIFIED error : {e}")

        finally:
            check_stop(VTT_WAIT)


def cancel_all_vtts(accsor, amin_client, ri_client):
    ri_vtt_orders = ri_client.vtt_order(VTT_ORDERS).get(VTT_ORDER_DATA)
    for ele in ri_vtt_orders:
        if ele.get(INITIAL_ORDER_STATUS) in ORDER_REJECTED_STATUS:
            continue
        else:
            accsor.cancel_vtt(ele.get(VTT_ORDER_ID))


