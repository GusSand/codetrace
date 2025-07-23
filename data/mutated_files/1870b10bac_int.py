from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "str"
from typing import Tuple, Callable

from protoactor.persistence.messages import Snapshot
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class __typ2(AbstractProvider):
    def __init__(__tmp0):
        __tmp0._events = {}

    async def get_snapshot(__tmp0, actor_name: __typ1) :
        return Snapshot, 0

    async def get_events(__tmp0, actor_name: __typ1, index_start, __tmp2,
                         callback) :
        if events := __tmp0._events.get(actor_name):
            for e in events:
                if index_start <= e.key <= __tmp2:
                    callback(e.value)
        return 0

    async def __tmp1(__tmp0, actor_name: __typ1, index: <FILL>, __tmp3) :
        events = __tmp0._events.setdefault(actor_name, {})
        next_event_index = 1
        if len(events) != 0:
            next_event_index = list(events.items())[-1][0] + 1
        events[next_event_index] = __tmp3
        return 0

    async def persist_snapshot(__tmp0, actor_name, index: int, snapshot) :
        pass

    async def delete_events(__tmp0, actor_name, inclusive_to_index: int) :
        events = __tmp0._events.get(actor_name)
        if events is None:
            pass
        events_to_remove = list(filter(lambda s: s.key <= inclusive_to_index, events.items()))
        for __tmp3 in events_to_remove:
            del __tmp0._events[__tmp3.key]

    async def delete_snapshots(__tmp0, actor_name, inclusive_to_index: int) :
        pass
