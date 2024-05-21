# https://www.youtube.com/watch?v=GMBt_4QQb5Y

from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils

dt_now = datetime.now(timezone("Asia/Kolkata"))
LogUtils("/opt/tmp/5paisa/5p_api_{}.log".format(dt_now.strftime('%Y-%m-%d')))

logger_obj = LogUtils.return_logger(__name__)
logger_obj.info('Starting algo now !!')

from paisa_5.p5_accesor import P5_Accessor
from paisa_5.ops_vtt import copy_vtts
from paisa_5.p5_utils import prepare_conns

AMIN_TOTP = '096136'
RI_TOTP =  284564

amin_client, ri_client = prepare_conns(AMIN_TOTP, RI_TOTP)
accsor = P5_Accessor(amin_client, ri_client)

copy_vtts(accsor, amin_client, ri_client)

