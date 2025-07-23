from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
# -*- coding: utf-8 -*-

from zerver.models import UserProfile, UserActivity, UserActivityInterval, Message

from django.utils.timezone import utc
from typing import Any, Dict, List, Sequence, Set

from datetime import datetime, timedelta

# Return the amount of Zulip usage for this user between the two
# given dates
def __tmp1(__tmp0: __typ0, __tmp2: <FILL>, end) :
    intervals = UserActivityInterval.objects.filter(__tmp0=__tmp0,
                                                    end__gte=__tmp2,
                                                    start__lte=end)
    duration = timedelta(0)
    for interval in intervals:
        start = max(__tmp2, interval.start)
        finish = min(end, interval.end)
        duration += finish-start
    return duration
