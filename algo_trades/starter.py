from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils

dt_now = datetime.now(timezone("Asia/Kolkata"))
LogUtils("/opt/tmp/angel_1/angel_api_{}.log".format(dt_now.strftime('%Y-%m-%d')))

logger_obj = LogUtils.return_logger(__name__)
logger_obj.info('Starting algo now !!')

from angel_one.angel_connector import AngelConnector
from strategies.weekly_expiry_all_legs import weekly_expiry_every_legs

conn = AngelConnector()
conn.generate_smart_api_session()
continue_setup = True


weekly_expiry_every_legs(conn)


# # #
# # df = conn.get_candlde_data('SBI-EQ')
# # #
# # print(df)
