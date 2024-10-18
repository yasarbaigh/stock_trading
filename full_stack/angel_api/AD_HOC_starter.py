from datetime import datetime

from pytz import timezone

from angel_one.configs import ADHOC_PROPERTIES
from common_utils.log_utils import LogUtils

dt_now = datetime.now(timezone("Asia/Kolkata"))
LogUtils("/opt/tmp/angel_1/angel_api_{}.log".format(dt_now.strftime('%Y-%m-%d')))

logger_obj = LogUtils.return_logger(__name__)
logger_obj.info('Starting algo now !!')
# ZZZ make sure u dont change above snippet
from angel_one.angel_connector import AngelConnector
from strategies.position_closer import close_positions
from strategies.ranga_strgy_expiry import ranga_weekly_expiry_every_legs_1
from jproperties import Properties

conn = AngelConnector()
conn.generate_smart_api_session()
continue_setup = True

configs = Properties()

with open(ADHOC_PROPERTIES, 'rb') as read_prop:
    configs.load(read_prop)

ranga_weekly_expiry_every_legs_1(conn, configs.get('adhoc_index').data, configs.get('adhoc_date_part').data)
close_positions(conn)
