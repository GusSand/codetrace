from typing import TypeAlias
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "BucketType"
import datetime
from typing import Dict
from .event import Event
from .bucket_type import BucketType


class __typ2:
    def __init__(__tmp1,
                 bucket_type,
                 timestamp,
                 event,
                 is_end: <FILL>
                 ) :
        __tmp1._bucket_type = bucket_type
        __tmp1._is_end = is_end
        __tmp1.event = event
        __tmp1.timestamp = timestamp

    @property
    def __tmp2(__tmp1) :
        return __tmp1.event.data  # type: ignore

    @property
    def event_type(__tmp1) :
        return __tmp1._bucket_type

    def is_end(__tmp1) :
        return __tmp1._is_end

    def __tmp0(__tmp1, other) :
        if __tmp1.timestamp == other.timestamp:
            return __tmp1.event_type == __typ1.AFK \
                   and other.event_type != __typ1.AFK
        return __tmp1.timestamp < other.timestamp
