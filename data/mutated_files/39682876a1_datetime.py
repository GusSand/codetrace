from typing import TypeAlias
__typ1 : TypeAlias = "EventRepository"
__typ0 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"
from datetime import datetime
from typing import List, Dict
from analyze.event import Event
from analyze.event_repository import EventRepository

__typ4 = List[Event]


class __typ2:
    def __init__(__tmp0, event_repository: __typ1) -> None:
        __tmp0.event_repository = event_repository
        __tmp0.events_cache: Dict[__typ0, __typ4] = {}
        __tmp0.cached_start_time = datetime.now()

    def get_bucket_events(__tmp0, buckets,
                          start_time: datetime, __tmp2: <FILL>
                          ) :
        if not __tmp0._cached_time_matches(start_time):
            __tmp0.events_cache.clear()
            __tmp0.cached_start_time = start_time

        events = {}
        for bucket_name in buckets:
            events[bucket_name] = __tmp0.get_events(
                bucket_name,
                start_time,
                __tmp2
            )

        return events

    def get_events(__tmp0, __tmp1, start_time,
                   __tmp2) -> __typ4:
        if __tmp1 not in __tmp0.events_cache \
                or len(__tmp0.events_cache[__tmp1]) == 0:
            events = __tmp0.event_repository.get_events(__tmp1,
                                                      start_time,
                                                      __tmp2)
        else:
            original_events = __tmp0.events_cache[__tmp1]
            last_event = original_events[0]
            next_start_time = last_event.timestamp.astimezone(tz=None)
            next_events = __tmp0.event_repository.get_events(
                __tmp1,
                next_start_time,
                __tmp2
            )
            next_ids = [event.id for event in reversed(next_events)]
            if last_event.id not in next_ids:
                # no merging required
                events = next_events + original_events
            else:
                last_position = len(next_ids) - next_ids.index(
                    last_event.id) - 1
                original_events[0] = next_events[last_position]
                if last_position == len(next_ids) - 1:
                    events = next_events + original_events[1:]
                else:
                    events = next_events[:last_position] + original_events

        __tmp0.events_cache[__tmp1] = events

        return events

    def _cached_time_matches(__tmp0, compared_time: datetime) :
        cached_time = __tmp0.cached_start_time.replace(microsecond=0, second=0)
        compared_time = compared_time.replace(microsecond=0, second=0)

        return cached_time == compared_time
