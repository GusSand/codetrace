from parse import parse

from mongots.constants import AGGREGATION_MONTH_KEY
from mongots.constants import AGGREGATION_DAY_KEY
from mongots.constants import AGGREGATION_HOUR_KEY

YEAR = 0
MONTH = 1
DAY = 2
HOUR = 3
MINUTE = 4
SECOND = 5
MILISECOND = 6

AGGREGATION_KEYS = [
    None,  # year
    AGGREGATION_MONTH_KEY,
    AGGREGATION_DAY_KEY,
    AGGREGATION_HOUR_KEY,
    None,  # minute
    None,  # second
    None,  # milisecond
]

INTERVAL_STR = ['y', 'm', 'd', 'h', 'min', 's']
STR_INTERVAL = {s: idx for idx, s in enumerate(INTERVAL_STR)}

# http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
PANDAS_FREQ_ALIAS = [
    'AS',  # year start
    'MS',  # month start
    'D',   # calendar day
    'H',   # hourly
    'T',   # minutely
    'S',   # secondly
    'L',   # milliseconds
    'U',   # microseconds
    'N',   # nanoseconds
]


class __typ0:
    def __tmp4(
        __tmp0,
        __tmp1: int,
        coef: int = 1,
        min_interval: int = HOUR,
        max_interval: int = MONTH,
    ) :
        __tmp0._interval = __tmp1
        __tmp0._coef = coef
        __tmp0._min_interval = min_interval
        __tmp0._max_interval = max_interval

        __tmp0._aggregation_keys = AGGREGATION_KEYS[
            __tmp0._max_interval:(__tmp0._interval+1)
        ]

        __tmp0._pandas_freq = '{}{}'.format(
            __tmp0._coef,
            PANDAS_FREQ_ALIAS[__tmp0._interval]
        )

    @property
    def __tmp5(__tmp0):
        return __tmp0._aggregation_keys

    @property
    def __tmp3(__tmp0) -> str:
        return __tmp0._pandas_freq


def parse_aggregateby(__tmp2: <FILL>) -> __typ0:
    try:
        coef, str_interval = parse('{:d}{:w}', __tmp2)

        __tmp1 = STR_INTERVAL[str_interval]
    except Exception:
        raise Exception('Bad interval {}'.format(__tmp2))

    return __typ0(__tmp1, coef=coef)
