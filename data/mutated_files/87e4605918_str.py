from typing import TypeAlias
__typ0 : TypeAlias = "PID"
__typ1 : TypeAlias = "bool"
import logging
from typing import Tuple

from protoactor.actor import log
from protoactor.actor.actor_context import Actor, AbstractContext, GlobalRootContext
from protoactor.actor.event_stream import GlobalEventStream
from protoactor.actor.messages import Started
from protoactor.actor.props import Props
from protoactor.actor.protos_pb2 import Terminated, PID
from protoactor.actor.supervision import Supervision
from protoactor.actor.utils import Singleton
from protoactor.cluster.member_status_events import AbstractMemberStatusEvent, MemberLeftEvent, MemberRejoinedEvent
from protoactor.cluster.messages import WatchPidRequest


class PidCache(metaclass=Singleton):
    def __tmp6(__tmp1):
        __tmp1._watcher = None
        __tmp1._cluster_topology_evn_sub = None
        __tmp1._cache = {}
        __tmp1._reverse_cache = {}

    async def __tmp5(__tmp1) :
        props = Props.from_producer(lambda: __typ2()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp1._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp1._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp1.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp1) :
        await GlobalRootContext.stop(__tmp1._watcher)
        GlobalEventStream.unsubscribe(__tmp1._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp1, __tmp0) :
        if isinstance(__tmp0, (MemberLeftEvent, MemberRejoinedEvent)):
            __tmp1.remove_cache_by_member_address(__tmp0.address)

    def __tmp2(__tmp1, __tmp8: str) :
        if __tmp8 in __tmp1._cache:
            return __tmp1._cache[__tmp8], True
        return None, False

    async def __tmp4(__tmp1, __tmp8: str, pid) -> __typ1:
        if __tmp8 not in __tmp1._cache:
            key = pid.to_short_string()
            __tmp1._cache[__tmp8] = pid
            __tmp1._reverse_cache[key] = __tmp8

            await GlobalRootContext.send(__tmp1._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp1, pid: __typ0) :
        key = pid.to_short_string()
        if key in __tmp1._reverse_cache:
            __tmp8 = __tmp1._reverse_cache[key]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp8]

    def __tmp3(__tmp1, __tmp8: <FILL>) :
        if __tmp8 in __tmp1._cache:
            key = __tmp1._cache[__tmp8]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp8]

    def remove_cache_by_member_address(__tmp1, member_address: str) -> None:
        for __tmp8, pid in __tmp1._cache.items():
            if pid.address == member_address:
                key = pid.to_short_string()
                del __tmp1._reverse_cache[key]
                del __tmp1._cache[__tmp8]


class __typ2(Actor):
    def __tmp6(__tmp1):
        __tmp1._logger = log.create_logger(logging.INFO, context=__typ2)

    async def __tmp7(__tmp1, context: AbstractContext) -> None:
        msg = context.message
        if isinstance(msg, Started):
            __tmp1._logger.debug('Started PidCacheWatcher')
        elif isinstance(msg, WatchPidRequest):
            await context.watch(msg.pid)
        elif isinstance(msg, Terminated):
            PidCache().remove_cache_by_pid(msg.who)
