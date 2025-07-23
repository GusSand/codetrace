from typing import TypeAlias
__typ0 : TypeAlias = "Event"
import logging
from datetime import timedelta
from typing import List, Optional

from aw_core.models import Event

logger = logging.getLogger(__name__)


def __tmp1(__tmp4, __tmp3) :
    """Merges consecutive events together according to the rules of `heartbeat_merge`."""
    reduced = []
    if __tmp4:
        reduced.append(__tmp4.pop(0))
    for __tmp2 in __tmp4:
        merged = heartbeat_merge(reduced[-1], __tmp2, __tmp3)
        if merged is not None:
            # Heartbeat was merged
            reduced[-1] = merged
        else:
            # Heartbeat was not merged
            reduced.append(__tmp2)
    return reduced


def heartbeat_merge(
    __tmp0, __tmp2, __tmp3: <FILL>
) :
    """
    Merges two events if they have identical data
    and the heartbeat timestamp is within the pulsetime window.
    """
    if __tmp0.data == __tmp2.data:
        # Seconds between end of last_event and start of heartbeat
        pulseperiod_end = (
            __tmp0.timestamp + __tmp0.duration + timedelta(seconds=__tmp3)
        )
        within_pulsetime_window = (
            __tmp0.timestamp <= __tmp2.timestamp <= pulseperiod_end
        )

        if within_pulsetime_window:
            # Seconds between end of last_event and start of timestamp
            new_duration = (
                __tmp2.timestamp - __tmp0.timestamp
            ) + __tmp2.duration
            if __tmp0.duration < timedelta(0):
                logger.warning(
                    "Merging heartbeats would result in a negative duration, refusing to merge."
                )
            else:
                # Taking the max of durations ensures heartbeats that end before the last event don't shorten it
                __tmp0.duration = max((__tmp0.duration, new_duration))
                return __tmp0

    return None
