BASE_PREFIX = '/home/trys'


MASTER_FILE = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

MASTER_FILE_PATH = BASE_PREFIX + '/opt/tmp/angel_1/{}_OpenAPIScripMaster.json'
STOP_CHECK = BASE_PREFIX+ '/opt/tmp/angel_1/stop.txt'
STOPPED = BASE_PREFIX + '/opt/tmp/angel_1/stop.txt.stopped'
ADHOC_PROPERTIES = BASE_PREFIX + '/opt/tmp/angel_1/angel_adhoc.properties'

XCHANGE_NSE = 'NSE'
XCHANGE_BSE = 'BSE'

SEGMENT_NSE_FNO = 'NFO'

TYPE_BUY = 'BUY'
TYPE_SELL = 'SELL'

ORDER_MARKET = 'MARKET'
ORDER_LIMIT = 'LIMIT'

PRODCUT_TYPE_CARRY_FORWARD = 'CARRYFORWARD'
PRODCUT_TYPE_BRACKET_ORDER = 'BO'

VARIETY_AMO = 'AMO'
VARIETY_NORMAL = 'NORMAL'
VARIETY_BRACKET_ORDER = 'ROBO'


INSTRUMENT_NSE_OPTION_IDX = 'OPTIDX'
INSTRUMENT_NSE_OPTION_STK = 'OPTSTK'

INSTRUMENT_NSE_FUT_IDX = 'FUTIDX'
INSTRUMENT_NSE_FUT_STK = 'FUTSTK'

INTERVAL_1_MIN = 'ONE_MINUTE'
INTERVAL_3_MIN = 'THREE_MINUTE'
INTERVAL_5_MIN = 'FIVE_MINUTE'
INTERVAL_10_MIN = 'TEN_MINUTE'
INTERVAL_15_MIN = 'FIFTEEN_MINUTE'

DATE_FORMAT_FULL_HISTROIC_CANDLE_ = '%Y-%M-%d %H:%M'
DATE_FORMAT_DAY_HISTROIC_CANDLE = '%Y-%M-%d'
DATE_FORMAT_START_TIME = '09:15'
DATE_FORMAT_END_TIME = '15:30'

ALLOWED_ORDER_STATUS = ['open', 'complete', 'cancelled', 'rejected']
ORDER_COMPLETE = 'complete'
OPEN_POSITION_STATUS = 'open'

ANGEL_1_BSE = 'ANGEL_1_BSE'
ANGEL_1_NSE = 'ANGEL_1_NSE'

PREFIX_API = 'API_'
ZERO_REALIZED = '0.00'

STRATEGY_1_EXPIRY_LEG = 'API_On_Each_Rounded_Straddle'

STRATEGY_1_RANGA_ORDER_1 = 'API_RANGA_1_{}'
STRATEGY_1_RANGA_ORDER_1_PREFIX = 'API_RANGA_1_'
STRATEGY_1_RANGA_ORDER_2 = 'API_Ranga_Other_Legs_On_Each_Rounded_Straddle'

STRATEGY_2_PREVIOUS_INITIATED = 'API_On_Each_Rounded_Straddle'
