from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "AbstractContext"
__typ1 : TypeAlias = "PID"
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
    def __tmp5(__tmp0):
        __tmp0._watcher = None
        __tmp0._cluster_topology_evn_sub = None
        __tmp0._cache = {}
        __tmp0._reverse_cache = {}

    async def setup(__tmp0) :
        props = Props.from_producer(lambda: __typ3()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp0._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp0._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp0.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp0) :
        await GlobalRootContext.stop(__tmp0._watcher)
        GlobalEventStream.unsubscribe(__tmp0._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp0, evn: AbstractMemberStatusEvent) :
        if isinstance(evn, MemberLeftEvent) or isinstance(evn, MemberRejoinedEvent):
            __tmp0.remove_cache_by_member_address(evn.address)

    def __tmp1(__tmp0, __tmp7: str) :
        if __tmp7 in __tmp0._cache.keys():
            return __tmp0._cache[__tmp7], True
        else:
            return None, False

    async def __tmp4(__tmp0, __tmp7, pid) :
        if __tmp7 not in __tmp0._cache.keys():
            key = pid.to_short_string()
            __tmp0._cache[__tmp7] = pid
            __tmp0._reverse_cache[key] = __tmp7

            await GlobalRootContext.send(__tmp0._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp0, pid) :
        key = pid.to_short_string()
        if key in __tmp0._reverse_cache:
            __tmp7 = __tmp0._reverse_cache[key]
            del __tmp0._reverse_cache[key]
            del __tmp0._cache[__tmp7]

    def __tmp2(__tmp0, __tmp7: <FILL>) -> None:
        if __tmp7 in __tmp0._cache:
            key = __tmp0._cache[__tmp7]
            del __tmp0._reverse_cache[key]
            del __tmp0._cache[__tmp7]

    def remove_cache_by_member_address(__tmp0, __tmp3) :
        for __tmp7, pid in __tmp0._cache.items():
            if pid.address == __tmp3:
                key = pid.to_short_string()
                del __tmp0._reverse_cache[key]
                del __tmp0._cache[__tmp7]


class __typ3(Actor):
    def __tmp5(__tmp0):
        __tmp0._logger = None

    async def __tmp6(__tmp0, context: __typ0) :
        msg = context.message
        if isinstance(msg, Started):
            # self._logger.log_debug('Started PidCacheWatcher')
            pass
        elif isinstance(msg, WatchPidRequest):
            await context.watch(msg.pid)
        elif isinstance(msg, Terminated):
            PidCache().remove_cache_by_pid(msg.who)
