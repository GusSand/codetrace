from typing import List, Callable, Any

from protoactor.actor import PID
from protoactor.actor.actor_context import GlobalRootContext
from protoactor.actor.message_envelope import MessageEnvelope
from protoactor.actor.props import Props
from protoactor.router.hash import HashRing
from protoactor.router.messages import AbstractHashable
from protoactor.router.router_config import GroupRouterConfig, PoolRouterConfig
from protoactor.router.router_state import RouterState


class ConsistentHashGroupRouterConfig(GroupRouterConfig):
    def __init__(__tmp0, __tmp5: Callable[[str], int], __tmp1, routees):
        super().__init__()
        if __tmp1 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp0._hash_func = __tmp5
        __tmp0._replica_count = __tmp1
        __tmp0._routees = routees

    def create_router_state(__tmp0) -> RouterState:
        return ConsistentHashRouterState(__tmp0._hash_func, __tmp0._replica_count)


class ConsistentHashPoolRouterConfig(PoolRouterConfig):
    def __init__(__tmp0, __tmp2, routee_props: Props, __tmp5: Callable[[str], int], __tmp1: int):
        super().__init__(__tmp2, routee_props)
        if __tmp1 <= 0:
            raise ValueError('ReplicaCount must be greater than 0')

        __tmp0._hash_func = __tmp5
        __tmp0._replica_count = __tmp1

    def create_router_state(__tmp0) -> RouterState:
        return ConsistentHashRouterState(__tmp0._hash_func, __tmp0._replica_count)


class ConsistentHashRouterState(RouterState):
    def __init__(__tmp0, __tmp5, __tmp1: int):
        __tmp0._hash_func = __tmp5
        __tmp0._replica_count = __tmp1
        __tmp0._hash_ring = None
        __tmp0._routee_map = None

    def __tmp4(__tmp0) :
        return list(__tmp0._routee_map.values())

    def __tmp3(__tmp0, routees: List[PID]) :
        __tmp0._routee_map = {}
        nodes = []

        for pid in routees:
            node_name = pid.to_short_string()
            nodes.append(node_name)
            __tmp0._routee_map[node_name] = pid

        __tmp0._hash_ring = HashRing(nodes, __tmp0._hash_func, __tmp0._replica_count)

    async def route_message(__tmp0, message: <FILL>) :
        msg, _, _ = MessageEnvelope.unwrap(message)
        if isinstance(msg, AbstractHashable):
            key = msg.hash_by()
            node = __tmp0._hash_ring.get_node(key)
            routee = __tmp0._routee_map[node]
            await GlobalRootContext.send(routee, message)
        else:
            raise AttributeError('Message of type %s does not implement AbstractHashable' % type(message).__name__)
