from typing import TypeAlias
__typ1 : TypeAlias = "RouterState"
__typ4 : TypeAlias = "Any"
__typ3 : TypeAlias = "Props"
from typing import List, Callable, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.message_envelope import MessageEnvelope
from protoactor.actor.props import Props
from protoactor.router.hash import HashRing
from protoactor.router.messages import AbstractHashable
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ2(GroupRouterConfig):
    def __init__(__tmp1, __tmp7: Callable[[str], int], __tmp2: <FILL>, routees):
        super().__init__()
        if __tmp2 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp1._hash_func = __tmp7
        __tmp1._replica_count = __tmp2
        __tmp1._routees = routees

    def __tmp6(__tmp1) :
        return __typ0(__tmp1._hash_func, __tmp1._replica_count)


class __typ5(PoolRouterConfig):
    def __init__(__tmp1, pool_size, __tmp3, __tmp7, __tmp2: int):
        super().__init__(pool_size, __tmp3)
        if __tmp2 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp1._hash_func = __tmp7
        __tmp1._replica_count = __tmp2

    def __tmp6(__tmp1) :
        return __typ0(__tmp1._hash_func, __tmp1._replica_count)


class __typ0(__typ1):
    def __init__(__tmp1, __tmp7: Callable[[str], int], __tmp2: int):
        __tmp1._hash_func = __tmp7
        __tmp1._replica_count = __tmp2
        __tmp1._hash_ring = None
        __tmp1._routee_map = None

    def __tmp5(__tmp1) :
        return list(__tmp1._routee_map.values())

    def __tmp4(__tmp1, routees: List[PID]) :
        __tmp1._routee_map = {}
        nodes = []

        for pid in routees:
            node_name = pid.to_short_string()
            nodes.append(node_name)
            __tmp1._routee_map[node_name] = pid

        __tmp1._hash_ring = HashRing(nodes, __tmp1._hash_func, __tmp1._replica_count)

    async def __tmp0(__tmp1, message: __typ4) -> None:
        msg, _, _ = MessageEnvelope.unwrap(message)
        if isinstance(msg, AbstractHashable):
            key = msg.hash_by()
            node = __tmp1._hash_ring.get_node(key)
            routee = __tmp1._routee_map[node]
            await GlobalRootContext.send(routee, message)
        else:
            raise AttributeError('Message of type %s does not implement AbstractHashable' % type(message).__name__)
