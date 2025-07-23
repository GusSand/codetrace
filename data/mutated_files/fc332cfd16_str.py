from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "int"
from typing import Tuple, Callable

from protoactor.persistence.messages import Snapshot
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class InMemoryProvider(AbstractProvider):
    def __tmp7(__tmp0):
        __tmp0._events = {}

    async def get_snapshot(__tmp0, __tmp8) :
        return Snapshot, 0

    async def __tmp3(__tmp0, __tmp8, index_start, index_end,
                         __tmp5) :
        if events := __tmp0._events.get(__tmp8):
            for e in events:
                if index_start <= e.key <= index_end:
                    __tmp5(e.value)
        return 0

    async def __tmp4(__tmp0, __tmp8, __tmp9, __tmp2) -> __typ1:
        events = __tmp0._events.setdefault(__tmp8, {})
        next_event_index = 1
        if len(events) != 0:
            next_event_index = list(events.items())[-1][0] + 1
        events[next_event_index] = __tmp2
        return 0

    async def __tmp6(__tmp0, __tmp8, __tmp9, snapshot) :
        pass

    async def delete_events(__tmp0, __tmp8, inclusive_to_index) :
        events = __tmp0._events.get(__tmp8)
        if events is None:
            pass
        events_to_remove = list(filter(lambda s: s.key <= inclusive_to_index, events.items()))
        for __tmp2 in events_to_remove:
            del __tmp0._events[__tmp2.key]

    async def __tmp1(__tmp0, __tmp8: <FILL>, inclusive_to_index) :
        pass
