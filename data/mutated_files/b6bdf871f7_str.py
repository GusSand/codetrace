from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "int"
from typing import Tuple, Callable

from protoactor.persistence.messages import Snapshot
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class __typ2(AbstractProvider):
    def __init__(self):
        self._events = {}

    async def get_snapshot(self, __tmp1) :
        return Snapshot, 0

    async def get_events(self, __tmp1, index_start, __tmp0,
                         callback) -> __typ1:
        if events := self._events.get(__tmp1):
            for e in events:
                if index_start <= e.key <= __tmp0:
                    callback(e.value)
        return 0

    async def persist_event(self, __tmp1: <FILL>, index, event: __typ0) -> __typ1:
        events = self._events.setdefault(__tmp1, {})
        next_event_index = 1
        if len(events) != 0:
            next_event_index = list(events.items())[-1][0] + 1
        events[next_event_index] = event
        return 0

    async def persist_snapshot(self, __tmp1: str, index, snapshot: __typ0) -> None:
        pass

    async def delete_events(self, __tmp1: str, inclusive_to_index: __typ1) -> None:
        events = self._events.get(__tmp1)
        if events is None:
            pass
        events_to_remove = list(filter(lambda s: s.key <= inclusive_to_index, events.items()))
        for event in events_to_remove:
            del self._events[event.key]

    async def delete_snapshots(self, __tmp1, inclusive_to_index) :
        pass
