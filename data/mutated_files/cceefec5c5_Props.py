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
    def new_broadcast_group(__tmp0: List[PID]) -> Props:
        return BroadcastGroupRouterConfig(__tmp0).props()

    @staticmethod
    def new_consistent_hash_group(__tmp0: List[PID],
                                  hash_func: Callable[[str], __typ0] = None,
                                  replica_count: __typ0 = None) :

        if hash_func is None and replica_count is None:
            return ConsistentHashGroupRouterConfig(MD5Hasher.hash, 100, __tmp0).props()
        return ConsistentHashGroupRouterConfig(hash_func, replica_count, __tmp0).props()

    @staticmethod
    def new_random_group(__tmp0, seed: __typ0 = None) -> Props:
        return RandomGroupRouterConfig(__tmp0, seed).props()

    @staticmethod
    def new_round_robin_group(__tmp0: List[PID]) :
        return RoundRobinGroupRouterConfig(__tmp0).props()

    @staticmethod
    def new_broadcast_pool(props: Props, __tmp1) :
        return BroadcastPoolRouterConfig(__tmp1, props).props()

    @staticmethod
    def __tmp2(props: <FILL>,
                                 __tmp1,
                                 hash_func: Callable[[str], __typ0] = None,
                                 replica_count: __typ0 = 100) -> Props:

        if hash_func is None:
            return ConsistentHashPoolRouterConfig(__tmp1, props, MD5Hasher.hash, replica_count).props()
        return ConsistentHashPoolRouterConfig(__tmp1, props, hash_func, replica_count).props()

    @staticmethod
    def new_random_pool(props: Props, __tmp1, seed: __typ0 = None) :
        return RandomPoolRouterConfig(__tmp1, props, seed).props()

    @staticmethod
    def new_round_robin_pool(props, __tmp1) -> Props:
        return RoundRobinPoolRouterConfig(__tmp1, props).props()
