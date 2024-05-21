API_KEY = 'URlbOmbB'
USERNAME = 'VVMTA1032'
LOGIN_CODE = '2468'
APP_TOKEN_KEY = 'IDDYSN2ODWM27OIBJ4DQC7BMXU'


WAIT_TIME = 20
NIFTY_50 = 'NIFTY_50'
FIN_NIFTY = 'FINNIFTY'
BANK_NIFTY = 'BANKNIFTY'
MID_CP_NIFTY = 'MIDCPNIFTY'
SENSEX = 'SENSEX'

TOKEN_NIFTY_50 = 99926000
TOKEN_BANK_NIFTY = 99926009
TOKEN_FIN_NIFTY = 99926037
TOKEN_MID_CP_NIFTY = 99926074
TOKEN_SENSEX = 99919000



INDEX_TOKEN_IDS = {
    NIFTY_50: {'exchange': 'NSE', 'tradingsymbol': 'Nifty 50', 'symboltoken': TOKEN_NIFTY_50, 'option_step': 50,
               'first_step': 50, 'second_step': 100, 'third_step': 200, 'fourth_step': 300, 'prefix': 'NIFTY{}{}{}',
               'order_lots': 1},

    BANK_NIFTY: {'exchange': 'NSE', 'tradingsymbol': 'Nifty Bank', 'symboltoken': TOKEN_BANK_NIFTY, 'option_step': 100,
                 'first_step': 100, 'second_step': 300, 'third_step': 300, 'fourth_step': 300,
                 'prefix': 'BANKNIFTY{}{}{}', 'order_lots': 1},

    FIN_NIFTY: {'exchange': 'NSE', 'tradingsymbol': 'Nifty Fin Service', 'symboltoken': TOKEN_FIN_NIFTY,
                'option_step': 50, 'first_step': 50, 'second_step': 100, 'third_step': 200, 'fourth_step': 300,
                'prefix': 'FINNIFTY{}{}{}', 'order_lots': 1},

    MID_CP_NIFTY: {'exchange': 'NSE', 'tradingsymbol': 'NIFTY MID SELECT', 'symboltoken': TOKEN_MID_CP_NIFTY,
                   'option_step': 25, 'first_step': 25, 'second_step': 50, 'third_step': 100, 'fourth_step': 150,
                   'prefix': 'MIDCPNIFTY{}{}{}', 'order_lots': 1},

    # MIDCPNIFTY08APR2410875CE

    SENSEX: {'exchange': 'BSE', 'tradingsymbol': 'SENSEX', 'symboltoken': TOKEN_SENSEX, 'option_step': 100,
             'first_step': 100, 'second_step': 300, 'third_step': 600, 'fourth_step': 900, 'prefix': 'SENSEX{}{}{}',
             'order_lots': 1},
}
