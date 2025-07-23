from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "Props"
from typing import List, Callable, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.message_envelope import MessageEnvelope
from protoactor.actor.props import Props
from protoactor.router.hash import HashRing
from protoactor.router.messages import AbstractHashable
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ3(GroupRouterConfig):
    def __init__(__tmp1, __tmp9, __tmp2, __tmp3):
        super().__init__()
        if __tmp2 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp1._hash_func = __tmp9
        __tmp1._replica_count = __tmp2
        __tmp1._routees = __tmp3

    def __tmp8(__tmp1) :
        return __typ0(__tmp1._hash_func, __tmp1._replica_count)


class ConsistentHashPoolRouterConfig(PoolRouterConfig):
    def __init__(__tmp1, __tmp4, __tmp5, __tmp9, __tmp2):
        super().__init__(__tmp4, __tmp5)
        if __tmp2 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp1._hash_func = __tmp9
        __tmp1._replica_count = __tmp2

    def __tmp8(__tmp1) :
        return __typ0(__tmp1._hash_func, __tmp1._replica_count)


class __typ0(RouterState):
    def __init__(__tmp1, __tmp9, __tmp2: <FILL>):
        __tmp1._hash_func = __tmp9
        __tmp1._replica_count = __tmp2
        __tmp1._hash_ring = None
        __tmp1._routee_map = None

    def __tmp7(__tmp1) -> List[PID]:
        return list(__tmp1._routee_map.values())

    def __tmp6(__tmp1, __tmp3) -> None:
        __tmp1._routee_map = {}
        nodes = []

        for pid in __tmp3:
            node_name = pid.to_short_string()
            nodes.append(node_name)
            __tmp1._routee_map[node_name] = pid

        __tmp1._hash_ring = HashRing(nodes, __tmp1._hash_func, __tmp1._replica_count)

    async def __tmp0(__tmp1, message) :
        msg, _, _ = MessageEnvelope.unwrap(message)
        if isinstance(msg, AbstractHashable):
            key = msg.hash_by()
            node = __tmp1._hash_ring.get_node(key)
            routee = __tmp1._routee_map[node]
            await GlobalRootContext.send(routee, message)
        else:
            raise AttributeError('Message of type %s does not implement AbstractHashable' % type(message).__name__)
