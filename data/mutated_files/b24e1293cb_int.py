from typing import TypeAlias
__typ1 : TypeAlias = "Props"
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
    def __tmp4(__tmp1) -> __typ1:
        return BroadcastGroupRouterConfig(__tmp1).props()

    @staticmethod
    def __tmp8(__tmp1,
                                  hash_func: Callable[[str], int] = None,
                                  replica_count: int = None) :

        if hash_func is None and replica_count is None:
            return ConsistentHashGroupRouterConfig(MD5Hasher.hash, 100, __tmp1).props()
        return ConsistentHashGroupRouterConfig(hash_func, replica_count, __tmp1).props()

    @staticmethod
    def __tmp6(__tmp1, seed: int = None) :
        return RandomGroupRouterConfig(__tmp1, seed).props()

    @staticmethod
    def __tmp0(__tmp1) -> __typ1:
        return RoundRobinGroupRouterConfig(__tmp1).props()

    @staticmethod
    def __tmp5(props, __tmp2) :
        return BroadcastPoolRouterConfig(__tmp2, props).props()

    @staticmethod
    def new_consistent_hash_pool(props,
                                 __tmp2: <FILL>,
                                 hash_func: Callable[[str], int] = None,
                                 replica_count: int = 100) -> __typ1:

        if hash_func is None:
            return ConsistentHashPoolRouterConfig(__tmp2, props, MD5Hasher.hash, replica_count).props()
        return ConsistentHashPoolRouterConfig(__tmp2, props, hash_func, replica_count).props()

    @staticmethod
    def __tmp3(props, __tmp2, seed: int = None) :
        return RandomPoolRouterConfig(__tmp2, props, seed).props()

    @staticmethod
    def __tmp7(props: __typ1, __tmp2) -> __typ1:
        return RoundRobinPoolRouterConfig(__tmp2, props).props()
