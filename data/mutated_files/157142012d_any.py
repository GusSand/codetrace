from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
from typing import Tuple, Callable

from protoactor.persistence.messages import Snapshot
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class __typ2(AbstractProvider):
    def __init__(self):
        self._events = {}

    async def get_snapshot(self, __tmp6) :
        return Snapshot, 0

    async def get_events(self, __tmp6, __tmp3: __typ0, index_end,
                         callback: Callable[[any], None]) :
        if events := self._events.get(__tmp6):
            for e in events:
                if __tmp3 <= e.key <= index_end:
                    callback(e.value)
        return 0

    async def __tmp4(self, __tmp6, index: __typ0, __tmp1: any) -> __typ0:
        events = self._events.setdefault(__tmp6, {})
        next_event_index = 1
        if len(events) != 0:
            next_event_index = list(events.items())[-1][0] + 1
        events[next_event_index] = __tmp1
        return 0

    async def __tmp5(self, __tmp6, index, snapshot: <FILL>) :
        pass

    async def __tmp2(self, __tmp6, __tmp0) :
        events = self._events.get(__tmp6)
        if events is None:
            pass
        events_to_remove = list(filter(lambda s: s.key <= __tmp0, events.items()))
        for __tmp1 in events_to_remove:
            del self._events[__tmp1.key]

    async def delete_snapshots(self, __tmp6, __tmp0) :
        pass
