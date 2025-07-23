from typing import TypeAlias
__typ0 : TypeAlias = "Props"
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
    def new_broadcast_group(routees) :
        return BroadcastGroupRouterConfig(routees).props()

    @staticmethod
    def new_consistent_hash_group(routees,
                                  hash_func: Callable[[str], int] = None,
                                  replica_count: int = None) :

        if hash_func is None and replica_count is None:
            return ConsistentHashGroupRouterConfig(MD5Hasher.hash, 100, routees).props()
        return ConsistentHashGroupRouterConfig(hash_func, replica_count, routees).props()

    @staticmethod
    def new_random_group(routees, seed: int = None) :
        return RandomGroupRouterConfig(routees, seed).props()

    @staticmethod
    def new_round_robin_group(routees) :
        return RoundRobinGroupRouterConfig(routees).props()

    @staticmethod
    def new_broadcast_pool(props, __tmp0) :
        return BroadcastPoolRouterConfig(__tmp0, props).props()

    @staticmethod
    def new_consistent_hash_pool(props,
                                 __tmp0,
                                 hash_func: Callable[[str], int] = None,
                                 replica_count: int = 100) -> __typ0:

        if hash_func is None:
            return ConsistentHashPoolRouterConfig(__tmp0, props, MD5Hasher.hash, replica_count).props()
        return ConsistentHashPoolRouterConfig(__tmp0, props, hash_func, replica_count).props()

    @staticmethod
    def __tmp1(props, __tmp0, seed: int = None) -> __typ0:
        return RandomPoolRouterConfig(__tmp0, props, seed).props()

    @staticmethod
    def new_round_robin_pool(props, __tmp0: <FILL>) :
        return RoundRobinPoolRouterConfig(__tmp0, props).props()
