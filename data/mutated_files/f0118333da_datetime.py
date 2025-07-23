from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "timedelta"
# -*- coding: utf-8 -*-

from zerver.models import UserProfile, UserActivity, UserActivityInterval, Message

from django.utils.timezone import utc
from typing import Any, Dict, List, Sequence, Set

from datetime import datetime, timedelta

# Return the amount of Zulip usage for this user between the two
# given dates
def seconds_usage_between(user_profile, __tmp0, end: <FILL>) :
    intervals = UserActivityInterval.objects.filter(user_profile=user_profile,
                                                    end__gte=__tmp0,
                                                    start__lte=end)
    duration = __typ0(0)
    for interval in intervals:
        start = max(__tmp0, interval.start)
        finish = min(end, interval.end)
        duration += finish-start
    return duration
