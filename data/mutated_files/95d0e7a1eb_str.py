from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
from datetime import datetime, timedelta
from typing import List, Optional

from analytics.lib.counts import CountStat
from zerver.lib.timestamp import floor_to_day, floor_to_hour, verify_UTC

# If min_length is None, returns end_times from ceiling(start) to floor(end), inclusive.
# If min_length is greater than 0, pads the list to the left.
# So informally, time_range(Sep 20, Sep 22, day, None) returns [Sep 20, Sep 21, Sep 22],
# and time_range(Sep 20, Sep 22, day, 5) returns [Sep 18, Sep 19, Sep 20, Sep 21, Sep 22]
def time_range(start: __typ0, __tmp1: __typ0, __tmp0: <FILL>,
               min_length: Optional[int]) :
    verify_UTC(start)
    verify_UTC(__tmp1)
    if __tmp0 == CountStat.HOUR:
        __tmp1 = floor_to_hour(__tmp1)
        step = timedelta(hours=1)
    elif __tmp0 == CountStat.DAY:
        __tmp1 = floor_to_day(__tmp1)
        step = timedelta(days=1)
    else:
        raise AssertionError("Unknown frequency: %s" % (__tmp0,))

    times = []
    if min_length is not None:
        start = min(start, __tmp1 - (min_length-1)*step)
    current = __tmp1
    while current >= start:
        times.append(current)
        current -= step
    return list(reversed(times))
