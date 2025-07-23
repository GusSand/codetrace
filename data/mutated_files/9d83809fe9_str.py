import logging
from datetime import timedelta
from typing import List

from aw_core.models import Event

logger = logging.getLogger(__name__)


def __tmp1(
    __tmp2: List[Event], __tmp0: <FILL>, pulsetime: float = 5.0
) -> List[Event]:
    """
    "Chunks" adjacent events together which have the same value for a key, and stores the
    original events in the :code:`subevents` key of the new event.
    """
    chunked_events: List[Event] = []
    for event in __tmp2:
        if __tmp0 not in event.data:
            break
        timediff = timedelta(seconds=999999999)  # FIXME: ugly but works
        if len(chunked_events) > 0:
            timediff = event.timestamp - (__tmp2[-1].timestamp + __tmp2[-1].duration)
        if (
            len(chunked_events) > 0
            and chunked_events[-1].data[__tmp0] == event.data[__tmp0]
            and timediff < timedelta(seconds=pulsetime)
        ):
            chunked_event = chunked_events[-1]
            chunked_event.duration += event.duration
            chunked_event.data["subevents"].append(event)
        else:
            data = {__tmp0: event.data[__tmp0], "subevents": [event]}
            chunked_event = Event(
                timestamp=event.timestamp, duration=event.duration, data=data
            )
            chunked_events.append(chunked_event)

    return chunked_events
