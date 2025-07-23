from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "int"
from typing import Tuple, Callable

from protoactor.persistence.messages import Snapshot
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class __typ2(AbstractProvider):
    def __init__(self):
        self._events = {}

    async def get_snapshot(self, actor_name) :
        return Snapshot, 0

    async def get_events(self, actor_name: <FILL>, __tmp1, index_end,
                         callback) :
        if events := self._events.get(actor_name):
            for e in events:
                if __tmp1 <= e.key <= index_end:
                    callback(e.value)
        return 0

    async def persist_event(self, actor_name, index, event) :
        events = self._events.setdefault(actor_name, {})
        next_event_index = 1
        if len(events) != 0:
            next_event_index = list(events.items())[-1][0] + 1
        events[next_event_index] = event
        return 0

    async def persist_snapshot(self, actor_name, index, snapshot) :
        pass

    async def delete_events(self, actor_name, inclusive_to_index) :
        events = self._events.get(actor_name)
        if events is None:
            pass
        events_to_remove = list(filter(lambda s: s.key <= inclusive_to_index, events.items()))
        for event in events_to_remove:
            del self._events[event.key]

    async def __tmp0(self, actor_name, inclusive_to_index) :
        pass
