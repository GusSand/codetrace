from typing import TypeAlias
__typ1 : TypeAlias = "RouterState"
__typ4 : TypeAlias = "Any"
from typing import List, Any, Iterable

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ2(GroupRouterConfig):
    def __init__(__tmp1, __tmp2: List[PID]):
        super().__init__()
        __tmp1._routees = __tmp2

    def __tmp4(__tmp1) :
        return __typ3()


class __typ0(PoolRouterConfig):
    def __init__(__tmp1, pool_size: <FILL>, routee_props):
        super().__init__(pool_size, routee_props)

    def __tmp4(__tmp1) -> __typ1:
        return __typ3()


class __typ3(__typ1):
    def __init__(__tmp1):
        __tmp1._routees = None
        __tmp1._current_index = 0

    def __tmp5(__tmp1) :
        return list(__tmp1._routees)

    def __tmp3(__tmp1, __tmp2: Iterable[PID]) -> None:
        __tmp1._routees = __tmp2

    async def route_message(__tmp1, __tmp0: __typ4) -> None:
        i = __tmp1._current_index % len(__tmp1._routees)
        __tmp1._current_index += 1
        pid = __tmp1._routees[i]

        await GlobalRootContext.send(pid, __tmp0)