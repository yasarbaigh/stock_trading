import time
from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils
from paisa_5.p5_values import MIN_WAIT, WAIT_10_SEC
from paisa_5.p5_words import VTT_CANCEL, EXCH, EXCHTYPE, INITIAL_LIMIT_PRICE, QUANTITY, SYMBOL, \
    INITIAL_TRIGGER_PRICE, SCRIP_CODE, BUY, MATCHING_CONDITION, VTT_PLACE, DELV_INTRA, INTRA_DAY, QTY, SL_TRIGGER_RATE, \
    RATE, EXCH_TYPE, BUY_SELL, VTT_MODIFIED, VTT_ORDER_ID, VTT_ORDERS, VTT_ORDER_DATA, MESSAGE, \
    OK_RESP_MESSAGES


class P5_Accessor:

    def __init__(self, p5_client):
        self.logger_obj = LogUtils.return_logger(__name__)

        self.p5_client = p5_client

    def get_all_orders(self, ):
        time.sleep(MIN_WAIT)
        return self.p5_client.order_book()

    def get_all_positions(self, ):
        time.sleep(MIN_WAIT)
        return self.p5_client.positions()

    def get_all_vtts(self):
        time.sleep(MIN_WAIT)
        resp = self.p5_client.vtt_order(VTT_ORDERS)
        i = 0
        while resp.get(MESSAGE) not in OK_RESP_MESSAGES:
            time.sleep(WAIT_10_SEC + i)
            resp = self.p5_client.vtt_order(VTT_ORDERS)
            i += 1

        return resp.get(VTT_ORDER_DATA, [])

    def place_vtt(self, vtt_order):
        try:
            resp = self.p5_client.vtt_order(VTT_PLACE, Exch=vtt_order.get(EXCH), ExchType=vtt_order.get(EXCHTYPE),
                                            ScripCode=vtt_order.get(SCRIP_CODE), Symbol=vtt_order.get(SYMBOL),
                                            InitialLimitPrice=vtt_order.get(INITIAL_LIMIT_PRICE), BuySell=BUY,
                                            InitialTriggerPrice=vtt_order.get(INITIAL_TRIGGER_PRICE),
                                            Quantity=vtt_order.get(QUANTITY),
                                            MatchingCondition=vtt_order.get(MATCHING_CONDITION))

            self.logger_obj.info('VTT_PLACED_Resp: {}'.format(resp))
            time.sleep(MIN_WAIT)
        except Exception as e:
            self.logger_obj.error(f"VTT_PLACED Error : {e}")

    def modify_vtt(self, vtt_order):
        try:
            resp = self.p5_client.vtt_order(VTT_MODIFIED, VTTOrderId=vtt_order.get(VTT_ORDER_ID),
                                            InitialLimitPrice=vtt_order.get(INITIAL_LIMIT_PRICE),
                                            InitialTriggerPrice=vtt_order.get(INITIAL_TRIGGER_PRICE),
                                            Qty=vtt_order.get(QUANTITY),
                                            MatchingCondition=vtt_order.get(MATCHING_CONDITION))

            self.logger_obj.info('VTT_MODIFIED_Resp: {}'.format(resp))
            time.sleep(MIN_WAIT)
        except Exception as e:
            self.logger_obj.error(f"VTT_MODIFIED error : {e}")

    def cancel_vtt(self, ordr_id):
        try:
            self.p5_client.vtt_order(VTT_CANCEL, VTTOrderId=ordr_id)
            time.sleep(MIN_WAIT)
        except Exception as e:
            self.logger_obj.error(f"vtt place error : {e}")

    def create_order(self, ordr):
        try:

            dt_now = datetime.now(timezone("Asia/Kolkata"))
            AH = 'N'
            if dt_now.hour < 9 or dt_now.hour > 15:
                AH = 'Y'
            elif dt_now == 9 and dt_now.minute < 15:
                AH = 'Y'

            is_intra = True if ordr.get(DELV_INTRA) == INTRA_DAY else False

            self.logger_obj.info('Placing order: {}'.format(ordr))
            resp = self.p5_client.place_order(OrderType=ordr.get(BUY_SELL), Exchange=ordr.get(EXCH),
                                              ExchangeType=ordr.get(EXCH_TYPE), ScripCode=ordr.get(SCRIP_CODE),
                                              Qty=ordr.get(QTY), Price=ordr.get(RATE), IsIntraday=is_intra,
                                              AHPlaced=AH, StopLossPrice=ordr.get(SL_TRIGGER_RATE, 0))

            self.logger_obj.info('create_order_Resp: {}'.format(resp))
            time.sleep(MIN_WAIT)
        except Exception as e:
            self.logger_obj.error(f"CancelOrder error : {e}")

    def cancel_normal_order(self, order_id):
        try:
            resp = self.p5_client.cancel_order(exch_order_id=order_id)
            self.logger_obj.info('cancel_order_Resp: {}'.format(resp))
            time.sleep(MIN_WAIT)
        except Exception as e:
            self.logger_obj.error(f"CancelOrder error : {e}")
