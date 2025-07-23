from typing import TypeAlias
__typ1 : TypeAlias = "RouterState"
__typ3 : TypeAlias = "Props"
__typ5 : TypeAlias = "Any"
import random
from typing import List, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ4(GroupRouterConfig):
    def __init__(__tmp1, __tmp0: List[PID], seed: int = None):
        super().__init__()
        __tmp1._routees = __tmp0
        __tmp1._seed = seed

    def create_router_state(__tmp1) :
        return __typ0(__tmp1._seed)


class __typ2(PoolRouterConfig):
    def __init__(__tmp1, pool_size: <FILL>, routee_props: __typ3, seed: int = None):
        super().__init__(pool_size, routee_props)
        __tmp1._seed = seed

    def create_router_state(__tmp1) :
        return __typ0(__tmp1._seed)


class __typ0(__typ1):
    def __init__(__tmp1, seed: int = None):
        if seed is not None:
            random.seed(seed)
        __tmp1._routees = None

    def get_routees(__tmp1) -> List[PID]:
        return list(__tmp1._routees)

    def set_routees(__tmp1, __tmp0) :
        __tmp1._routees = __tmp0

    async def route_message(__tmp1, __tmp2) :
        i = random.randint(0, len(__tmp1._routees) - 1)
        pid = __tmp1._routees[i]
        await GlobalRootContext.send(pid, __tmp2)
