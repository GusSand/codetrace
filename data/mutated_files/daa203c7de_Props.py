from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import Callable, List

from protoactor.actor import PID
from protoactor.actor.props import Props
from protoactor.router.broadcast_router import BroadcastGroupRouterConfig, BroadcastPoolRouterConfig
from protoactor.router.consistent_hash_group_router import ConsistentHashGroupRouterConfig, \
    ConsistentHashPoolRouterConfig
from protoactor.router.hash import MD5Hasher
from protoactor.router.random_router import RandomGroupRouterConfig, RandomPoolRouterConfig
from protoactor.router.round_robin_router import RoundRobinGroupRouterConfig, RoundRobinPoolRouterConfig


class Router:
    @staticmethod
    def __tmp0(routees: List[PID]) -> Props:
        return BroadcastGroupRouterConfig(routees).props()

    @staticmethod
    def new_consistent_hash_group(routees: List[PID],
                                  hash_func: Callable[[str], __typ0] = None,
                                  replica_count: __typ0 = None) -> Props:

        if hash_func is None and replica_count is None:
            return ConsistentHashGroupRouterConfig(MD5Hasher.hash, 100, routees).props()
        return ConsistentHashGroupRouterConfig(hash_func, replica_count, routees).props()

    @staticmethod
    def new_random_group(routees: List[PID], seed: __typ0 = None) -> Props:
        return RandomGroupRouterConfig(routees, seed).props()

    @staticmethod
    def __tmp2(routees) -> Props:
        return RoundRobinGroupRouterConfig(routees).props()

    @staticmethod
    def new_broadcast_pool(props: <FILL>, __tmp1: __typ0) -> Props:
        return BroadcastPoolRouterConfig(__tmp1, props).props()

    @staticmethod
    def new_consistent_hash_pool(props: Props,
                                 __tmp1: __typ0,
                                 hash_func: Callable[[str], __typ0] = None,
                                 replica_count: __typ0 = 100) -> Props:

        if hash_func is None:
            return ConsistentHashPoolRouterConfig(__tmp1, props, MD5Hasher.hash, replica_count).props()
        return ConsistentHashPoolRouterConfig(__tmp1, props, hash_func, replica_count).props()

    @staticmethod
    def new_random_pool(props, __tmp1: __typ0, seed: __typ0 = None) -> Props:
        return RandomPoolRouterConfig(__tmp1, props, seed).props()

    @staticmethod
    def new_round_robin_pool(props: Props, __tmp1: __typ0) :
        return RoundRobinPoolRouterConfig(__tmp1, props).props()
