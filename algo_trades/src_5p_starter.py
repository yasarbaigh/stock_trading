import argparse
import time
from datetime import datetime

from pytz import timezone

from common_utils.log_utils import LogUtils
from paisa_5.p5_creds import CREDS_AMIN

dt_now = datetime.now(timezone("Asia/Kolkata"))
LogUtils("/opt/tmp/5paisa/source_api_{}.log".format(dt_now.strftime('%Y-%m-%d')))

logger_obj = LogUtils.return_logger(__name__)
logger_obj.info('Starting algo now !!')

from paisa_5.p5_accesor import P5_Accessor
from paisa_5.ops_source_entries import source_vtts, source_orders, clear_sources
from paisa_5.p5_utils import prepare_api_conns
from distutils import util
from paisa_5.p5_values import WAIT_25_SEC


def main():
    parser = argparse.ArgumentParser(description="5Paisa Configs")
    parser.add_argument("--source-totp", type=str, required=False)
    parser.add_argument("--get-vtts", type=util.strtobool, default=False, help="Get All Vtts")
    parser.add_argument("--clear-sources", type=util.strtobool, default=False, help="Clear caches")

    args = parser.parse_args()

    source_totp = args.source_totp if args.source_totp else '632187'

    src_client = prepare_api_conns(CREDS_AMIN, source_totp)
    accsor = P5_Accessor(src_client)

    try:
        continue_source_orders = True
        if args.get_vtts:
            source_vtts(accsor)
        while continue_source_orders:
            continue_source_orders = source_orders(accsor)
            logger_obj.info('Sourcing orders flag: {}'.format(continue_source_orders))

            time.sleep(WAIT_25_SEC)

    except Exception as e:
        logger_obj.error('Sourcing orders failed {}'.format(e))
    finally:
        if args.clear_sources:
            clear_sources()


if __name__ == "__main__":
    main()
