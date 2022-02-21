from pytz import timezone

TZ = timezone('US/Eastern')
JONES = 197757429948219392
WHODAT = 763412923409760296
MAX_MSG_LEN = 2000

# Log verbosity
LOG_TRIVIAL = -1
LOG_REGULAR = 0
LOG_CRITICAL = 9999


## Change this to change the logging behavior
LOG_V = LOG_REGULAR


RACETYPE_SYNC = "sync"
RACETYPE_ASYNC = "async"
RACETYPES = (RACETYPE_SYNC, RACETYPE_ASYNC)

RACE_ROOM_CLOSE_TIME = 30
RANDOM_ROOM_NAME_LENGTH = 6

RACE_PATH = "./races"
ADMINS = (JONES, WHODAT)