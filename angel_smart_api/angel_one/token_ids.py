API_KEY = ''
USERNAME = ''
LOGIN_CODE = ''
APP_TOKEN_KEY = ''


WAIT_TIME = 20
NIFTY_50 = 'NIFTY 50'
NIFTY_500 = 'NIFTY 500'
FIN_NIFTY = 'FINNIFTY'
BANK_NIFTY = 'BANKNIFTY'
MID_CP_NIFTY = 'MIDCPNIFTY'
SENSEX = 'SENSEX'

TOKEN_NIFTY_50 = 99926000
TOKEN_BANK_NIFTY = 99926009
TOKEN_FIN_NIFTY = 99926037
TOKEN_MID_CP_NIFTY = 99926074
TOKEN_SENSEX = 99926074

INDEX_TOKEN_IDS = {
    NIFTY_50: {'exchange': 'NSE', 'tradingsymbol': 'Nifty 50', 'symboltoken': '99926000', 'option_step': 50,
               'first_step': 50, 'second_step': 100, 'third_step': 200, 'prefix': 'NIFTY{}{}{}', 'order_lots': 1},

    # BANK_NIFTY: {'exchange': 'NSE', 'tradingsymbol': 'Nifty Bank', 'symboltoken': '99926009', 'option_step': 100,
    #              'first_step': 100, 'second_step': 300, 'prefix': 'SENSEX{}{}{}', 'order_lots': 1},

    FIN_NIFTY: {'exchange': 'NSE', 'tradingsymbol': 'Nifty Fin Service', 'symboltoken': '99926037', 'option_step': 50,
                'first_step': 50, 'second_step': 100, 'third_step': 200, 'order_lots': 1},

    MID_CP_NIFTY: {'exchange': 'NSE', 'tradingsymbol': 'NIFTY MID SELECT', 'symboltoken': '99926074', 'option_step': 25,
                   'first_step': 25, 'second_step': 50, 'third_step': 100, 'prefix': 'MIDCPNIFTY{}{}{}', 'order_lots': 1},
    # MIDCPNIFTY08APR2410875CE

    SENSEX: {'exchange': 'BSE', 'tradingsymbol': 'SENSEX', 'symboltoken': '0', 'option_step': 100,
             'first_step': 100, 'second_step': 300, 'third_step': 600, 'prefix': 'SENSEX{}{}{}', 'order_lots': 1},
}
