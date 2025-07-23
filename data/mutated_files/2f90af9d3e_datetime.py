from typing import TypeAlias
__typ2 : TypeAlias = "EventRepository"
__typ1 : TypeAlias = "str"
from datetime import datetime
from typing import List, Dict
from analyze.event import Event
from analyze.event_repository import EventRepository

__typ0 = List[Event]


class CachedEventRepository:
    def __init__(self, event_repository) -> None:
        self.event_repository = event_repository
        self.events_cache: Dict[__typ1, __typ0] = {}
        self.cached_start_time = datetime.now()

    def get_bucket_events(self, buckets,
                          __tmp0: <FILL>, __tmp1
                          ) :
        if not self._cached_time_matches(__tmp0):
            self.events_cache.clear()
            self.cached_start_time = __tmp0

        events = {}
        for bucket_name in buckets:
            events[bucket_name] = self.get_events(
                bucket_name,
                __tmp0,
                __tmp1
            )

        return events

    def get_events(self, bucket: __typ1, __tmp0: datetime,
                   __tmp1: datetime) :
        if bucket not in self.events_cache \
                or len(self.events_cache[bucket]) == 0:
            events = self.event_repository.get_events(bucket,
                                                      __tmp0,
                                                      __tmp1)
        else:
            original_events = self.events_cache[bucket]
            last_event = original_events[0]
            next_start_time = last_event.timestamp.astimezone(tz=None)
            next_events = self.event_repository.get_events(
                bucket,
                next_start_time,
                __tmp1
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

        self.events_cache[bucket] = events

        return events

    def _cached_time_matches(self, __tmp2) :
        cached_time = self.cached_start_time.replace(microsecond=0, second=0)
        __tmp2 = __tmp2.replace(microsecond=0, second=0)

        return cached_time == __tmp2
