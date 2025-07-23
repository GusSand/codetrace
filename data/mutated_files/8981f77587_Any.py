from typing import TypeAlias
__typ4 : TypeAlias = "Props"
__typ2 : TypeAlias = "RouterState"
__typ0 : TypeAlias = "int"
import random
from typing import List, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ5(GroupRouterConfig):
    def __init__(__tmp2, __tmp3, seed: __typ0 = None):
        super().__init__()
        __tmp2._routees = __tmp3
        __tmp2._seed = seed

    def __tmp7(__tmp2) -> __typ2:
        return __typ1(__tmp2._seed)


class __typ3(PoolRouterConfig):
    def __init__(__tmp2, __tmp4, __tmp5, seed: __typ0 = None):
        super().__init__(__tmp4, __tmp5)
        __tmp2._seed = seed

    def __tmp7(__tmp2) -> __typ2:
        return __typ1(__tmp2._seed)


class __typ1(__typ2):
    def __init__(__tmp2, seed: __typ0 = None):
        if seed is not None:
            random.seed(seed)
        __tmp2._routees = None

    def __tmp8(__tmp2) :
        return list(__tmp2._routees)

    def __tmp6(__tmp2, __tmp3) :
        __tmp2._routees = __tmp3

    async def __tmp1(__tmp2, __tmp0: <FILL>) :
        i = random.randint(0, len(__tmp2._routees) - 1)
        pid = __tmp2._routees[i]
        await GlobalRootContext.send(pid, __tmp0)
