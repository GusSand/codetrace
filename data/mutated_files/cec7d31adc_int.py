from typing import Tuple, Callable

from protoactor.persistence.messages import Snapshot
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class InMemoryProvider(AbstractProvider):
    def __tmp12(__tmp1):
        __tmp1._events = {}

    async def __tmp7(__tmp1, __tmp13) -> Tuple[any, int]:
        return Snapshot, 0

    async def __tmp6(__tmp1, __tmp13, __tmp8, __tmp2,
                         __tmp10) :
        if events := __tmp1._events.get(__tmp13):
            for e in events:
                if __tmp8 <= e.key <= __tmp2:
                    __tmp10(e.value)
        return 0

    async def __tmp9(__tmp1, __tmp13, __tmp15, __tmp4: any) -> int:
        events = __tmp1._events.setdefault(__tmp13, {})
        next_event_index = 1
        if len(events) != 0:
            next_event_index = list(events.items())[-1][0] + 1
        events[next_event_index] = __tmp4
        return 0

    async def __tmp11(__tmp1, __tmp13, __tmp15: int, __tmp14: any) -> None:
        pass

    async def __tmp5(__tmp1, __tmp13: str, __tmp0: int) :
        events = __tmp1._events.get(__tmp13)
        if events is None:
            pass
        events_to_remove = list(filter(lambda s: s.key <= __tmp0, events.items()))
        for __tmp4 in events_to_remove:
            del __tmp1._events[__tmp4.key]

    async def __tmp3(__tmp1, __tmp13, __tmp0: <FILL>) -> None:
        pass
