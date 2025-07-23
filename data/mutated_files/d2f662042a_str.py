
from typing import List

import pytz

def __tmp1() -> List[str]:
    return sorted(pytz.all_timezones)

def __tmp0(tz: <FILL>) :
    return pytz.timezone(tz)
