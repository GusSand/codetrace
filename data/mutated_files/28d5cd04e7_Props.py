from typing import TypeAlias
__typ0 : TypeAlias = "Router"
__typ1 : TypeAlias = "int"
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
    def __tmp5(__tmp1) :
        return BroadcastGroupRouterConfig(__tmp1).props()

    @staticmethod
    def __tmp9(__tmp1,
                                  hash_func: Callable[[str], __typ1] = None,
                                  replica_count: __typ1 = None) :

        if hash_func is None and replica_count is None:
            return ConsistentHashGroupRouterConfig(MD5Hasher.hash, 100, __tmp1).props()
        return ConsistentHashGroupRouterConfig(hash_func, replica_count, __tmp1).props()

    @staticmethod
    def __tmp6(__tmp1, seed: __typ1 = None) -> Props:
        return RandomGroupRouterConfig(__tmp1, seed).props()

    @staticmethod
    def __tmp0(__tmp1) -> Props:
        return RoundRobinGroupRouterConfig(__tmp1).props()

    @staticmethod
    def __tmp7(props: Props, __tmp2: __typ1) -> Props:
        return BroadcastPoolRouterConfig(__tmp2, props).props()

    @staticmethod
    def __tmp4(props,
                                 __tmp2,
                                 hash_func: Callable[[str], __typ1] = None,
                                 replica_count: __typ1 = 100) -> Props:

        if hash_func is None:
            return ConsistentHashPoolRouterConfig(__tmp2, props, MD5Hasher.hash, replica_count).props()
        return ConsistentHashPoolRouterConfig(__tmp2, props, hash_func, replica_count).props()

    @staticmethod
    def __tmp3(props: <FILL>, __tmp2: __typ1, seed: __typ1 = None) -> Props:
        return RandomPoolRouterConfig(__tmp2, props, seed).props()

    @staticmethod
    def __tmp8(props: Props, __tmp2) :
        return RoundRobinPoolRouterConfig(__tmp2, props).props()
