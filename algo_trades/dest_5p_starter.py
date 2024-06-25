# https://www.youtube.com/watch?v=GMBt_4QQb5Y

from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils

dt_now = datetime.now(timezone("Asia/Kolkata"))
LogUtils("/opt/tmp/5paisa/dest_api_{}.log".format(dt_now.strftime('%Y-%m-%d')))

logger_obj = LogUtils.return_logger(__name__)
logger_obj.info('Starting algo now !!')
from paisa_5.p5_creds import CREDS_AMIN, CREDS_RI
from distutils import util
from paisa_5.p5_accesor import P5_Accessor
from paisa_5.ops_vtt import copy_vtts, cancel_all_vtts
from paisa_5.p5_utils import prepare_api_conns
import argparse
from paisa_5.ops_ordrs import manage_orders


def main():
    parser = argparse.ArgumentParser(description="5Paisa Configs")

    parser.add_argument("--dest-totp", type=str, required=False)
    parser.add_argument("--vtt-cancel", type=util.strtobool, default=False, help="Cancel All Vtts")

    args = parser.parse_args()
    print('Cancell All Vtts : True') if args.vtt_cancel else print('Cancell All Vtts  : False')

    dest_totp = args.dest_totp if args.dest_totp else '246550'

    dest_client = prepare_api_conns( CREDS_RI, dest_totp)
    # Use above, DELTE Below conn
    # dest_client = prepare_api_conns(CREDS_AMIN, dest_totp)

    accsor = P5_Accessor(dest_client)

    if args.vtt_cancel:
        cancel_all_vtts(accsor)
    else:
        pass
        copy_vtts(accsor)

    manage_orders(accsor)


if __name__ == "__main__":
    main()
