from typing import TypeAlias
__typ1 : TypeAlias = "RouterState"
__typ0 : TypeAlias = "Any"
import random
from typing import List, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ3(GroupRouterConfig):
    def __init__(__tmp0, routees, seed: int = None):
        super().__init__()
        __tmp0._routees = routees
        __tmp0._seed = seed

    def create_router_state(__tmp0) -> __typ1:
        return __typ2(__tmp0._seed)


class RandomPoolRouterConfig(PoolRouterConfig):
    def __init__(__tmp0, pool_size, routee_props: <FILL>, seed: int = None):
        super().__init__(pool_size, routee_props)
        __tmp0._seed = seed

    def create_router_state(__tmp0) -> __typ1:
        return __typ2(__tmp0._seed)


class __typ2(__typ1):
    def __init__(__tmp0, seed: int = None):
        if seed is not None:
            random.seed(seed)
        __tmp0._routees = None

    def get_routees(__tmp0) -> List[PID]:
        return list(__tmp0._routees)

    def set_routees(__tmp0, routees: List[PID]) -> None:
        __tmp0._routees = routees

    async def route_message(__tmp0, message) :
        i = random.randint(0, len(__tmp0._routees) - 1)
        pid = __tmp0._routees[i]
        await GlobalRootContext.send(pid, message)
