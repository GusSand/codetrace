from datetime import datetime, timedelta
from typing import List, Optional

from analytics.lib.counts import CountStat
from zerver.lib.timestamp import floor_to_day, floor_to_hour, verify_UTC

# If min_length is None, returns end_times from ceiling(start) to floor(end), inclusive.
# If min_length is greater than 0, pads the list to the left.
# So informally, time_range(Sep 20, Sep 22, day, None) returns [Sep 20, Sep 21, Sep 22],
# and time_range(Sep 20, Sep 22, day, 5) returns [Sep 18, Sep 19, Sep 20, Sep 21, Sep 22]
def time_range(__tmp1: <FILL>, __tmp2: datetime, __tmp0: str,
               __tmp3: Optional[int]) :
    verify_UTC(__tmp1)
    verify_UTC(__tmp2)
    if __tmp0 == CountStat.HOUR:
        __tmp2 = floor_to_hour(__tmp2)
        step = timedelta(hours=1)
    elif __tmp0 == CountStat.DAY:
        __tmp2 = floor_to_day(__tmp2)
        step = timedelta(days=1)
    else:
        raise AssertionError("Unknown frequency: %s" % (__tmp0,))

    times = []
    if __tmp3 is not None:
        __tmp1 = min(__tmp1, __tmp2 - (__tmp3-1)*step)
    current = __tmp2
    while current >= __tmp1:
        times.append(current)
        current -= step
    return list(reversed(times))
