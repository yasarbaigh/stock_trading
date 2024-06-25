from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils
from common_utils.redis_utils import RedisHelper
from paisa_5.p5_utils import is_allowed_symbol, check_stop
from paisa_5.p5_values import MID_WAIT, WAIT_25_SEC
from paisa_5.p5_words import ORDER_REQUESTER_CODE, ORDER_5PVTT, BUY_SELL, B, S, \
    BUY_NUM, SYMBOL, RDS_VTT_KEY, ORDER_STATUS, REJECTED, RDS_ORDERS_KEY, INITIAL_ORDER_STATUS, ORDER_COMPLETED_STATUS

logger_obj = LogUtils.return_logger(__name__)

rds_clnt = RedisHelper()


def source_orders(accsor, ):
    try:
        output_orders = []
        for item in accsor.get_all_orders():
            if item.get(ORDER_REQUESTER_CODE) == ORDER_5PVTT or item.get(ORDER_STATUS) == REJECTED:

                # vtt order or rejected order so skip

                continue

            elif item.get(BUY_SELL) == B:
                output_orders.append(item)

            elif item.get(BUY_SELL) == S:
                # skipp sell orders

                continue
        logger_obj.info('source_ORDERS: \n\n {}'.format(output_orders))
        logger_obj.info('source_ORDERS count: \n\n {}'.format(len(output_orders)))

        rds_clnt.set_json(RDS_ORDERS_KEY, output_orders)

        dt_now = datetime.now(timezone("Asia/Kolkata"))

        # after market hours close sourcing
        return False if (dt_now.hour < 8 or dt_now.hour > 15) else True



    except Exception as e:
        logger_obj.error(f"source_ORDERS error : {e}")

    finally:
        check_stop(WAIT_25_SEC)


def source_vtts(accsor):
    try:

        output_vtts = []
        for item in accsor.get_all_vtts():
            if item.get(INITIAL_ORDER_STATUS) in ORDER_COMPLETED_STATUS:
                continue
            if item.get(BUY_SELL) == BUY_NUM and is_allowed_symbol(item.get(SYMBOL)):
                output_vtts.append(item)

                logger_obj.info('Sourced vtt : {}'.format(item.get(SYMBOL)))

        logger_obj.info('Total Sourced vtts : {}'.format(output_vtts))
        logger_obj.info('Total Sourced vtts count : {}'.format(len(output_vtts)))

        rds_clnt.set_json(RDS_VTT_KEY, output_vtts)


    except Exception as e:
        logger_obj.error(f"source_vtts error : {e}")

    finally:
        check_stop(WAIT_25_SEC)


def clear_sources():
    rds_clnt.set_json(RDS_VTT_KEY, [])
    rds_clnt.set_json(RDS_ORDERS_KEY, [])
