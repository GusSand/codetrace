from typing import TypeAlias
__typ1 : TypeAlias = "Any"
from typing import List, Any, Iterable

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class BroadcastGroupRouterConfig(GroupRouterConfig):
    def __init__(__tmp3, __tmp0):
        super().__init__()
        __tmp3._routees = __tmp0

    def __tmp2(__tmp3) -> RouterState:
        return __typ0()


class BroadcastPoolRouterConfig(PoolRouterConfig):
    def __init__(__tmp3, pool_size: int, routee_props: <FILL>):
        super().__init__(pool_size, routee_props)

    def __tmp2(__tmp3) :
        return __typ0()


class __typ0(RouterState):
    def __init__(__tmp3):
        __tmp3._routees = None

    def get_routees(__tmp3) :
        return list(__tmp3._routees)

    def set_routees(__tmp3, __tmp0) :
        __tmp3._routees = __tmp0

    async def __tmp1(__tmp3, message) :
        for pid in __tmp3._routees:
            await GlobalRootContext.send(pid, message)