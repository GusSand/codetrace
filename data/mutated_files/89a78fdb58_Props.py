from typing import TypeAlias
__typ0 : TypeAlias = "Router"
from typing import Callable, List

from protoactor.actor import PID
from protoactor.actor.props import Props
from protoactor.router.broadcast_router import BroadcastGroupRouterConfig, BroadcastPoolRouterConfig
from protoactor.router.consistent_hash_group_router import ConsistentHashGroupRouterConfig, \
    ConsistentHashPoolRouterConfig
from protoactor.router.hash import MD5Hasher
from protoactor.router.random_router import RandomGroupRouterConfig, RandomPoolRouterConfig
from protoactor.router.round_robin_router import RoundRobinGroupRouterConfig, RoundRobinPoolRouterConfig


class __typ0:
    @staticmethod
    def new_broadcast_group(routees) :
        return BroadcastGroupRouterConfig(routees).props()

    @staticmethod
    def new_consistent_hash_group(routees,
                                  hash_func: Callable[[str], int] = None,
                                  replica_count: int = None) -> Props:

        if hash_func is None and replica_count is None:
            return ConsistentHashGroupRouterConfig(MD5Hasher.hash, 100, routees).props()
        return ConsistentHashGroupRouterConfig(hash_func, replica_count, routees).props()

    @staticmethod
    def new_random_group(routees, seed: int = None) -> Props:
        return RandomGroupRouterConfig(routees, seed).props()

    @staticmethod
    def new_round_robin_group(routees) -> Props:
        return RoundRobinGroupRouterConfig(routees).props()

    @staticmethod
    def __tmp1(props: Props, __tmp0: int) -> Props:
        return BroadcastPoolRouterConfig(__tmp0, props).props()

    @staticmethod
    def new_consistent_hash_pool(props: Props,
                                 __tmp0,
                                 hash_func: Callable[[str], int] = None,
                                 replica_count: int = 100) -> Props:

        if hash_func is None:
            return ConsistentHashPoolRouterConfig(__tmp0, props, MD5Hasher.hash, replica_count).props()
        return ConsistentHashPoolRouterConfig(__tmp0, props, hash_func, replica_count).props()

    @staticmethod
    def new_random_pool(props, __tmp0, seed: int = None) -> Props:
        return RandomPoolRouterConfig(__tmp0, props, seed).props()

    @staticmethod
    def new_round_robin_pool(props: <FILL>, __tmp0: int) :
        return RoundRobinPoolRouterConfig(__tmp0, props).props()
