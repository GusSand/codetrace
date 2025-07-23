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
    def __tmp7(__tmp1):
        __tmp1._watcher = None
        __tmp1._cluster_topology_evn_sub = None
        __tmp1._cache = {}
        __tmp1._reverse_cache = {}

    async def __tmp6(__tmp1) :
        props = Props.from_producer(lambda: PidCacheWatcher()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp1._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp1._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp1.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp1) -> None:
        await GlobalRootContext.stop(__tmp1._watcher)
        GlobalEventStream.unsubscribe(__tmp1._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp1, __tmp0: AbstractMemberStatusEvent) :
        if isinstance(__tmp0, MemberLeftEvent) or isinstance(__tmp0, MemberRejoinedEvent):
            __tmp1.remove_cache_by_member_address(__tmp0.address)

    def __tmp3(__tmp1, __tmp9) :
        if __tmp9 in __tmp1._cache.keys():
            return __tmp1._cache[__tmp9], True
        else:
            return None, False

    async def __tmp4(__tmp1, __tmp9, pid) :
        if __tmp9 not in __tmp1._cache.keys():
            key = pid.to_short_string()
            __tmp1._cache[__tmp9] = pid
            __tmp1._reverse_cache[key] = __tmp9

            await GlobalRootContext.send(__tmp1._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp1, pid) :
        key = pid.to_short_string()
        if key in __tmp1._reverse_cache:
            __tmp9 = __tmp1._reverse_cache[key]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp9]

    def __tmp5(__tmp1, __tmp9) -> None:
        if __tmp9 in __tmp1._cache:
            key = __tmp1._cache[__tmp9]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp9]

    def remove_cache_by_member_address(__tmp1, member_address: <FILL>) :
        for __tmp9, pid in __tmp1._cache.items():
            if pid.address == member_address:
                key = pid.to_short_string()
                del __tmp1._reverse_cache[key]
                del __tmp1._cache[__tmp9]


class PidCacheWatcher(Actor):
    def __tmp7(__tmp1):
        __tmp1._logger = None

    async def __tmp8(__tmp1, __tmp2) :
        msg = __tmp2.message
        if isinstance(msg, Started):
            # self._logger.log_debug('Started PidCacheWatcher')
            pass
        elif isinstance(msg, WatchPidRequest):
            await __tmp2.watch(msg.pid)
        elif isinstance(msg, Terminated):
            PidCache().remove_cache_by_pid(msg.who)
