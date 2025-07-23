from typing import TypeAlias
__typ2 : TypeAlias = "Props"
__typ3 : TypeAlias = "int"
__typ0 : TypeAlias = "RouterState"
from typing import List, Any, Iterable

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.props import Props
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class RoundRobinGroupRouterConfig(GroupRouterConfig):
    def __init__(__tmp2, __tmp3):
        super().__init__()
        __tmp2._routees = __tmp3

    def __tmp7(__tmp2) :
        return __typ1()


class RoundRobinPoolRouterConfig(PoolRouterConfig):
    def __init__(__tmp2, __tmp4, __tmp5):
        super().__init__(__tmp4, __tmp5)

    def __tmp7(__tmp2) :
        return __typ1()


class __typ1(__typ0):
    def __init__(__tmp2):
        __tmp2._routees = None
        __tmp2._current_index = 0

    def __tmp8(__tmp2) :
        return list(__tmp2._routees)

    def __tmp6(__tmp2, __tmp3) :
        __tmp2._routees = __tmp3

    async def __tmp1(__tmp2, __tmp0: <FILL>) :
        i = __tmp2._current_index % len(__tmp2._routees)
        __tmp2._current_index += 1
        pid = __tmp2._routees[i]

        await GlobalRootContext.send(pid, __tmp0)