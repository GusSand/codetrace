from typing import TypeAlias
__typ0 : TypeAlias = "float"
import logging
from datetime import timedelta
from typing import List, Optional

from aw_core.models import Event

logger = logging.getLogger(__name__)


def __tmp1(__tmp5, __tmp4: __typ0) :
    """Merges consecutive events together according to the rules of `heartbeat_merge`."""
    reduced = []
    if __tmp5:
        reduced.append(__tmp5.pop(0))
    for __tmp3 in __tmp5:
        merged = __tmp2(reduced[-1], __tmp3, __tmp4)
        if merged is not None:
            # Heartbeat was merged
            reduced[-1] = merged
        else:
            # Heartbeat was not merged
            reduced.append(__tmp3)
    return reduced


def __tmp2(
    __tmp0, __tmp3: <FILL>, __tmp4
) :
    """
    Merges two events if they have identical data
    and the heartbeat timestamp is within the pulsetime window.
    """
    if __tmp0.data == __tmp3.data:
        # Seconds between end of last_event and start of heartbeat
        pulseperiod_end = (
            __tmp0.timestamp + __tmp0.duration + timedelta(seconds=__tmp4)
        )
        within_pulsetime_window = (
            __tmp0.timestamp <= __tmp3.timestamp <= pulseperiod_end
        )

        if within_pulsetime_window:
            # Seconds between end of last_event and start of timestamp
            new_duration = (
                __tmp3.timestamp - __tmp0.timestamp
            ) + __tmp3.duration
            if __tmp0.duration < timedelta(0):
                logger.warning(
                    "Merging heartbeats would result in a negative duration, refusing to merge."
                )
            else:
                # Taking the max of durations ensures heartbeats that end before the last event don't shorten it
                __tmp0.duration = max((__tmp0.duration, new_duration))
                return __tmp0

    return None
