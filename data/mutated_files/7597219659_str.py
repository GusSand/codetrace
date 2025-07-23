from typing import TypeAlias
__typ2 : TypeAlias = "AbstractMemberStatusEvent"
__typ0 : TypeAlias = "AbstractContext"
from typing import Tuple

from protoactor.actor.actor import Actor, AbstractContext, GlobalRootContext
from protoactor.actor.event_stream import GlobalEventStream
from protoactor.actor.messages import Started
from protoactor.actor.props import Props
from protoactor.actor.protos_pb2 import Terminated, PID
from protoactor.actor.supervision import Supervision
from protoactor.actor.utils import Singleton
from protoactor.сluster.member_status_events import AbstractMemberStatusEvent, MemberLeftEvent, MemberRejoinedEvent
from protoactor.сluster.messages import WatchPidRequest


class PidCache(metaclass=Singleton):
    def __tmp6(__tmp1):
        __tmp1._watcher = None
        __tmp1._cluster_topology_evn_sub = None
        __tmp1._cache = {}
        __tmp1._reverse_cache = {}

    async def __tmp5(__tmp1) -> None:
        props = Props.from_producer(lambda: __typ1()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp1._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp1._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp1.process_member_status_event,
                                                                     type(__typ2))

    async def stop(__tmp1) :
        await GlobalRootContext.stop(__tmp1._watcher)
        GlobalEventStream.unsubscribe(__tmp1._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp1, __tmp0: __typ2) -> None:
        if isinstance(__tmp0, MemberLeftEvent) or isinstance(__tmp0, MemberRejoinedEvent):
            __tmp1.remove_cache_by_member_address(__tmp0.address)

    def __tmp2(__tmp1, __tmp8: <FILL>) :
        if __tmp8 in __tmp1._cache.keys():
            return __tmp1._cache[__tmp8], True
        else:
            return None, False

    async def __tmp4(__tmp1, __tmp8, pid: PID) -> bool:
        if __tmp8 not in __tmp1._cache.keys():
            key = pid.to_short_string()
            __tmp1._cache[__tmp8] = pid
            __tmp1._reverse_cache[key] = __tmp8

            await GlobalRootContext.send(__tmp1._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp1, pid: PID) -> None:
        key = pid.to_short_string()
        if key in __tmp1._reverse_cache:
            __tmp8 = __tmp1._reverse_cache[key]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp8]

    def remove_cache_by_name(__tmp1, __tmp8: str) -> None:
        if __tmp8 in __tmp1._cache:
            key = __tmp1._cache[__tmp8]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp8]

    def remove_cache_by_member_address(__tmp1, member_address: str) :
        for __tmp8, pid in __tmp1._cache.items():
            if pid.address == member_address:
                key = pid.to_short_string()
                del __tmp1._reverse_cache[key]
                del __tmp1._cache[__tmp8]


class __typ1(Actor):
    def __tmp6(__tmp1):
        __tmp1._logger = None

    async def __tmp7(__tmp1, __tmp3) :
        msg = __tmp3.message
        if isinstance(msg, Started):
            # self._logger.log_debug('Started PidCacheWatcher')
            pass
        elif isinstance(msg, WatchPidRequest):
            await __tmp3.watch(msg.pid)
        elif isinstance(msg, Terminated):
            PidCache().remove_cache_by_pid(msg.who)
