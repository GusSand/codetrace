from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from typing import List, Any, Iterable

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class BroadcastGroupRouterConfig(GroupRouterConfig):
    def __init__(__tmp2, __tmp3):
        super().__init__()
        __tmp2._routees = __tmp3

    def __tmp5(__tmp2) -> RouterState:
        return BroadcastRouterState()


class BroadcastPoolRouterConfig(PoolRouterConfig):
    def __init__(__tmp2, __tmp4: <FILL>, routee_props):
        super().__init__(__tmp4, routee_props)

    def __tmp5(__tmp2) -> RouterState:
        return BroadcastRouterState()


class BroadcastRouterState(RouterState):
    def __init__(__tmp2):
        __tmp2._routees = None

    def __tmp6(__tmp2) :
        return list(__tmp2._routees)

    def set_routees(__tmp2, __tmp3) :
        __tmp2._routees = __tmp3

    async def __tmp1(__tmp2, __tmp0) :
        for pid in __tmp2._routees:
            await GlobalRootContext.send(pid, __tmp0)