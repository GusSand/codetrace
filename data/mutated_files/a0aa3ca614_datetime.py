from typing import TypeAlias
__typ0 : TypeAlias = "str"
from datetime import datetime
from typing import List, Dict
from analyze.event import Event
from analyze.event_repository import EventRepository

Events = List[Event]


class CachedEventRepository:
    def __init__(__tmp1, event_repository: EventRepository) :
        __tmp1.event_repository = event_repository
        __tmp1.events_cache: Dict[__typ0, Events] = {}
        __tmp1.cached_start_time = datetime.now()

    def get_bucket_events(__tmp1, __tmp0: List[__typ0],
                          __tmp2: datetime, end_time
                          ) -> Dict[__typ0, Events]:
        if not __tmp1._cached_time_matches(__tmp2):
            __tmp1.events_cache.clear()
            __tmp1.cached_start_time = __tmp2

        events = {}
        for bucket_name in __tmp0:
            events[bucket_name] = __tmp1.get_events(
                bucket_name,
                __tmp2,
                end_time
            )

        return events

    def get_events(__tmp1, bucket: __typ0, __tmp2: datetime,
                   end_time: <FILL>) -> Events:
        if bucket not in __tmp1.events_cache \
                or len(__tmp1.events_cache[bucket]) == 0:
            events = __tmp1.event_repository.get_events(bucket,
                                                      __tmp2,
                                                      end_time)
        else:
            original_events = __tmp1.events_cache[bucket]
            last_event = original_events[0]
            next_start_time = last_event.timestamp.astimezone(tz=None)
            next_events = __tmp1.event_repository.get_events(
                bucket,
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

        __tmp1.events_cache[bucket] = events

        return events

    def _cached_time_matches(__tmp1, compared_time: datetime) -> bool:
        cached_time = __tmp1.cached_start_time.replace(microsecond=0, second=0)
        compared_time = compared_time.replace(microsecond=0, second=0)

        return cached_time == compared_time
