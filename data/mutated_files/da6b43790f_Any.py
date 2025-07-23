from typing import TypeAlias
__typ0 : TypeAlias = "RouterState"
from typing import List, Any, Iterable

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class BroadcastGroupRouterConfig(GroupRouterConfig):
    def __init__(__tmp1, routees):
        super().__init__()
        __tmp1._routees = routees

    def create_router_state(__tmp1) :
        return BroadcastRouterState()


class __typ1(PoolRouterConfig):
    def __init__(__tmp1, __tmp0, routee_props):
        super().__init__(__tmp0, routee_props)

    def create_router_state(__tmp1) :
        return BroadcastRouterState()


class BroadcastRouterState(__typ0):
    def __init__(__tmp1):
        __tmp1._routees = None

    def get_routees(__tmp1) :
        return list(__tmp1._routees)

    def set_routees(__tmp1, routees) :
        __tmp1._routees = routees

    async def route_message(__tmp1, message: <FILL>) :
        for pid in __tmp1._routees:
            await GlobalRootContext.send(pid, message)