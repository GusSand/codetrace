from typing import TypeAlias
__typ0 : TypeAlias = "PersistedEvent"
__typ1 : TypeAlias = "bool"
import datetime
from datetime import timedelta
from typing import Callable

from protoactor.persistence.messages import PersistedEvent
from protoactor.persistence.snapshot_strategies.abstract_snapshot_strategy import AbstractSnapshotStrategy


class TimeStrategy(AbstractSnapshotStrategy):
    def __init__(__tmp0, __tmp1: <FILL>, get_now: Callable[[], datetime.datetime] = None):
        __tmp0._interval = __tmp1
        if get_now is None:
            __tmp0._get_now = lambda: datetime.datetime.now()
        else:
            __tmp0._get_now = get_now
        __tmp0._last_taken = __tmp0._get_now()

    def should_take_snapshot(__tmp0, persisted_event) :
        now = __tmp0._get_now()
        if (__tmp0._last_taken + __tmp0._interval) <= now:
            __tmp0._last_taken = now
            return True

        return False
