import json
import os
import time

from py5paisa import FivePaisaClient

from common_utils.log_utils import LogUtils
from paisa_5.p5_creds import p5_amin_client_code, p5_amin_creds, p5_amin_pin, p5_ri_client_code, p5_ri_pin, p5_ri_creds, \
    INVALID_SCRIPTS, CREDS
from paisa_5.p5_values import P5_STOP_CHECK, P5_STOPPED, P5_DIR
from paisa_5.p5_words import EXCHTYPE, SCRIP_CODE, INITIAL_LIMIT_PRICE, BUY_SELL, MATCHING_CONDITION, QUANTITY, \
    INITIAL_TRIGGER_PRICE, EXCH, SYMBOL

logger_obj = LogUtils.return_logger(__name__)


def prepare_conns(amin_totp, ri_totp):
    ri_client = FivePaisaClient(cred=p5_ri_creds)
    if ri_totp:
        ri_client = FivePaisaClient(cred=p5_ri_creds)
        ri_client.get_totp_session(p5_ri_client_code, ri_totp, p5_ri_pin)
        ri_client.get_oauth_session('Your Response Token')
        logger_obj.info("R---IIIIII Token : {}".format(ri_client.get_access_token()))

    amin_client = FivePaisaClient(cred=p5_amin_creds)
    if amin_totp:
        amin_client.get_totp_session(p5_amin_client_code, amin_totp, p5_amin_pin)
        amin_client.get_oauth_session('Your Response Token')
        logger_obj.info("Amin Token : {}".format(amin_client.get_access_token()))

    return amin_client, ri_client


def prepare_api_conns(creds_key, totp):
    api_client = FivePaisaClient(cred=CREDS.get(creds_key).get('app_config'))
    api_client.get_totp_session(CREDS.get(creds_key).get('client_code'), totp, CREDS.get(creds_key).get('pin'))
    api_client.get_oauth_session('Your Response Token')
    logger_obj.info("{} Token : {}".format(creds_key, api_client.get_access_token()))
    return api_client


def clone_vtt_order(src_vtt, is_modified=False):
    try:
        new_vtt = {INITIAL_LIMIT_PRICE: float(src_vtt.get(INITIAL_LIMIT_PRICE)) - .05,
                   INITIAL_TRIGGER_PRICE: float(src_vtt.get(INITIAL_TRIGGER_PRICE)) - .05}
    except Exception as e:
        logger_obj.error('Error in clonning price {}'.format(e))
        new_vtt = {INITIAL_LIMIT_PRICE: 0, INITIAL_TRIGGER_PRICE: float(src_vtt.get(INITIAL_TRIGGER_PRICE)) - .05}

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
    search_symbl = search_symbl.strip().lower()
    if search_symbl and '2024' in search_symbl and 'ce' not in search_symbl and 'pe' not in search_symbl:
        # Futures entry
        return False

    search_symbl = search_symbl.split(' ')
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


def export_to_json(file_name, content):
    with open(P5_DIR.format(file_name), 'w', encoding='utf-8') as f:
        json.dump(list(content), f, ensure_ascii=False, indent=4)
