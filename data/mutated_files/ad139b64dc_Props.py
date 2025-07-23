from typing import TypeAlias
__typ2 : TypeAlias = "RouterState"
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "Any"
from typing import List, Any, Iterable

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ3(GroupRouterConfig):
    def __init__(self, __tmp0):
        super().__init__()
        self._routees = __tmp0

    def __tmp2(self) -> __typ2:
        return __typ4()


class __typ1(PoolRouterConfig):
    def __init__(self, pool_size, __tmp1: <FILL>):
        super().__init__(pool_size, __tmp1)

    def __tmp2(self) :
        return __typ4()


class __typ4(__typ2):
    def __init__(self):
        self._routees = None
        self._current_index = 0

    def get_routees(self) :
        return list(self._routees)

    def set_routees(self, __tmp0) :
        self._routees = __tmp0

    async def route_message(self, message) :
        i = self._current_index % len(self._routees)
        self._current_index += 1
        pid = self._routees[i]

        await GlobalRootContext.send(pid, message)