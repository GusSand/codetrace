from typing import TypeAlias
__typ0 : TypeAlias = "EventRepository"
from datetime import datetime
from typing import List, Dict
from analyze.event import Event
from analyze.event_repository import EventRepository

Events = List[Event]


class __typ1:
    def __init__(__tmp1, event_repository: __typ0) -> None:
        __tmp1.event_repository = event_repository
        __tmp1.events_cache: Dict[str, Events] = {}
        __tmp1.cached_start_time = datetime.now()

    def __tmp0(__tmp1, buckets,
                          __tmp3: datetime, end_time: datetime
                          ) -> Dict[str, Events]:
        if not __tmp1._cached_time_matches(__tmp3):
            __tmp1.events_cache.clear()
            __tmp1.cached_start_time = __tmp3

        events = {}
        for bucket_name in buckets:
            events[bucket_name] = __tmp1.get_events(
                bucket_name,
                __tmp3,
                end_time
            )

        return events

    def get_events(__tmp1, __tmp2, __tmp3: <FILL>,
                   end_time) :
        if __tmp2 not in __tmp1.events_cache \
                or len(__tmp1.events_cache[__tmp2]) == 0:
            events = __tmp1.event_repository.get_events(__tmp2,
                                                      __tmp3,
                                                      end_time)
        else:
            original_events = __tmp1.events_cache[__tmp2]
            last_event = original_events[0]
            next_start_time = last_event.timestamp.astimezone(tz=None)
            next_events = __tmp1.event_repository.get_events(
                __tmp2,
                next_start_time,
                end_time
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

        __tmp1.events_cache[__tmp2] = events

        return events

    def _cached_time_matches(__tmp1, compared_time: datetime) -> bool:
        cached_time = __tmp1.cached_start_time.replace(microsecond=0, second=0)
        compared_time = compared_time.replace(microsecond=0, second=0)

        return cached_time == compared_time
