import os
import time

from py5paisa import FivePaisaClient

from common_utils.log_utils import LogUtils
from paisa_5.p5_creds import p5_amin_client_code, p5_amin_creds, p5_amin_pin, p5_ri_client_code, p5_ri_pin, p5_ri_creds, \
    INVALID_SCRIPTS
from paisa_5.p5_values import P5_STOP_CHECK, P5_STOPPED
from paisa_5.p5_words import EXCHTYPE, SCRIP_CODE, INITIAL_LIMIT_PRICE, BUY_SELL, MATCHING_CONDITION, QUANTITY, \
    INITIAL_TRIGGER_PRICE, EXCH, SYMBOL

logger_obj = LogUtils.return_logger(__name__)


def prepare_conns(amin_totp, ri_totp):
    ri_client = FivePaisaClient(cred=p5_ri_creds)
    ri_client.get_totp_session(p5_ri_client_code, ri_totp, p5_ri_pin)

    ri_client.get_oauth_session('Your Response Token')
    logger_obj.info("R---IIIIII Token : {}".format(ri_client.get_access_token()))

    amin_client = FivePaisaClient(cred=p5_amin_creds)
    amin_client.get_totp_session(p5_amin_client_code, amin_totp, p5_amin_pin)

    amin_client.get_oauth_session('Your Response Token')

    logger_obj.info("Amin Token : {}".format(amin_client.get_access_token()))

    return amin_client, ri_client


def clone_vtt_order(src_vtt, is_modified=False):
    new_vtt = {INITIAL_LIMIT_PRICE: src_vtt.get(INITIAL_LIMIT_PRICE)}
    new_vtt[INITIAL_TRIGGER_PRICE] = src_vtt.get(INITIAL_TRIGGER_PRICE)
    new_vtt[QUANTITY] = src_vtt.get(QUANTITY)
    new_vtt[MATCHING_CONDITION] = src_vtt.get(MATCHING_CONDITION)
    if is_modified:
        # vtt-id to be copied
        pass
    else:
        new_vtt[BUY_SELL] = src_vtt.get(BUY_SELL)
        new_vtt[SYMBOL] = src_vtt.get(SYMBOL)
        new_vtt[EXCH] = src_vtt.get(EXCH)
        new_vtt[EXCHTYPE] = src_vtt.get(EXCHTYPE)
        new_vtt[SCRIP_CODE] = src_vtt.get(SCRIP_CODE)
    return new_vtt


def is_allowed_symbol(search_symbl):
    search_symbl = search_symbl.strip().lower().split(' ')

    if search_symbl[0] in INVALID_SCRIPTS:
        return False

    return True


def check_stop(wait_time):
    if os.path.isfile(P5_STOP_CHECK):
        logger_obj.info(f"Stop exist, so exiting : {P5_STOP_CHECK}")
        os.rename(P5_STOP_CHECK, P5_STOPPED)
        exit(0)
    else:
        time.sleep(wait_time)
