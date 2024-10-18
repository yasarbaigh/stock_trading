import time
from datetime import datetime

from pytz import timezone

from angel_one.configs import ORDER_COMPLETE, TYPE_SELL, TYPE_BUY, ZERO_REALIZED, PREFIX_API
from common_utils.log_utils import LogUtils

logger_objt = LogUtils.return_logger(__name__)


def close_positions(conn, ):
    dt_now = datetime.now(timezone("Asia/Kolkata"))

    while dt_now.hour != 15:
        time.sleep(55)
        dt_now = datetime.now(timezone("Asia/Kolkata"))

    while dt_now.minute < 15:
        time.sleep(55)
        dt_now = datetime.now(timezone("Asia/Kolkata"))
        logger_objt.info('Checking next iteration for exit positions.')

    logger_objt.info('Exit positions started.')

    time.sleep(1)
    orders = conn.get_orders()

    postns = conn.get_positions()

    logger_objt.info(orders)
    logger_objt.info(postns)
    open_positions = {}

    if orders.get('data'):
        for item in orders.get('data'):
            if (item.get('ordertag') and item.get('ordertag').startswith(PREFIX_API) and
                    ORDER_COMPLETE == item.get('orderstatus')):

                if item.get('transactiontype') == TYPE_SELL:
                    open_positions[item.get('tradingsymbol')] = item
                elif item.get('transactiontype') == TYPE_BUY and open_positions.get(item.get('tradingsymbol')):
                    open_positions.pop(item.get('transactiontype'), None)
                else:
                    pass

    if postns.get('data'):
        for k, item in open_positions.items():
            for pos in postns.get('data', []):
                if pos.get('tradingsymbol') == item.get('tradingsymbol') and pos.get('realised') == ZERO_REALIZED:
                    logger_objt.info('Exiting for order: {}'.format(item))
                    conn.order_placment(my_exchange=item.get('exchange'), my_symbol=item.get('tradingsymbol'),
                                        my_token=item.get('symboltoken'), my_type=TYPE_BUY, my_price=0,
                                        my_quantity=item.get('quantity'), my_ordertag='Exit_' + item.get('ordertag'))
                    time.sleep(.5)

    open_positions = {}
    logger_objt.info('Exiting close positions')
