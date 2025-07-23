from typing import TypeAlias
__typ2 : TypeAlias = "int"
from typing import List, Callable, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.message_envelope import MessageEnvelope
from protoactor.actor.props import Props
from protoactor.router.hash import HashRing
from protoactor.router.messages import AbstractHashable
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class __typ1(GroupRouterConfig):
    def __init__(__tmp0, __tmp6, __tmp1, __tmp2):
        super().__init__()
        if __tmp1 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp0._hash_func = __tmp6
        __tmp0._replica_count = __tmp1
        __tmp0._routees = __tmp2

    def __tmp5(__tmp0) :
        return __typ0(__tmp0._hash_func, __tmp0._replica_count)


class __typ3(PoolRouterConfig):
    def __init__(__tmp0, pool_size, __tmp3: <FILL>, __tmp6, __tmp1):
        super().__init__(pool_size, __tmp3)
        if __tmp1 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp0._hash_func = __tmp6
        __tmp0._replica_count = __tmp1

    def __tmp5(__tmp0) :
        return __typ0(__tmp0._hash_func, __tmp0._replica_count)


class __typ0(RouterState):
    def __init__(__tmp0, __tmp6, __tmp1):
        __tmp0._hash_func = __tmp6
        __tmp0._replica_count = __tmp1
        __tmp0._hash_ring = None
        __tmp0._routee_map = None

    def get_routees(__tmp0) :
        return list(__tmp0._routee_map.values())

    def __tmp4(__tmp0, __tmp2) :
        __tmp0._routee_map = {}
        nodes = []

        for pid in __tmp2:
            node_name = pid.to_short_string()
            nodes.append(node_name)
            __tmp0._routee_map[node_name] = pid

        __tmp0._hash_ring = HashRing(nodes, __tmp0._hash_func, __tmp0._replica_count)

    async def route_message(__tmp0, message) :
        msg, _, _ = MessageEnvelope.unwrap(message)
        if isinstance(msg, AbstractHashable):
            key = msg.hash_by()
            node = __tmp0._hash_ring.get_node(key)
            routee = __tmp0._routee_map[node]
            await GlobalRootContext.send(routee, message)
        else:
            raise AttributeError('Message of type %s does not implement AbstractHashable' % type(message).__name__)
