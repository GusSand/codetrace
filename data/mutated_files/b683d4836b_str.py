from typing import TypeAlias
__typ2 : TypeAlias = "PID"
__typ0 : TypeAlias = "AbstractContext"
__typ3 : TypeAlias = "bool"
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


class __typ1(metaclass=Singleton):
    def __tmp4(__tmp0):
        __tmp0._watcher = None
        __tmp0._cluster_topology_evn_sub = None
        __tmp0._cache = {}
        __tmp0._reverse_cache = {}

    async def __tmp3(__tmp0) :
        props = Props.from_producer(lambda: PidCacheWatcher()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp0._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp0._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp0.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp0) :
        await GlobalRootContext.stop(__tmp0._watcher)
        GlobalEventStream.unsubscribe(__tmp0._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp0, evn) :
        if isinstance(evn, (MemberLeftEvent, MemberRejoinedEvent)):
            __tmp0.remove_cache_by_member_address(evn.address)

    def get_cache(__tmp0, __tmp6) :
        if __tmp6 in __tmp0._cache:
            return __tmp0._cache[__tmp6], True
        return None, False

    async def __tmp1(__tmp0, __tmp6: <FILL>, pid) :
        if __tmp6 not in __tmp0._cache:
            key = pid.to_short_string()
            __tmp0._cache[__tmp6] = pid
            __tmp0._reverse_cache[key] = __tmp6

            await GlobalRootContext.send(__tmp0._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp0, pid: __typ2) -> None:
        key = pid.to_short_string()
        if key in __tmp0._reverse_cache:
            __tmp6 = __tmp0._reverse_cache[key]
            del __tmp0._reverse_cache[key]
            del __tmp0._cache[__tmp6]

    def remove_cache_by_name(__tmp0, __tmp6) :
        if __tmp6 in __tmp0._cache:
            key = __tmp0._cache[__tmp6]
            del __tmp0._reverse_cache[key]
            del __tmp0._cache[__tmp6]

    def remove_cache_by_member_address(__tmp0, __tmp2: str) :
        for __tmp6, pid in __tmp0._cache.items():
            if pid.address == __tmp2:
                key = pid.to_short_string()
                del __tmp0._reverse_cache[key]
                del __tmp0._cache[__tmp6]


class PidCacheWatcher(Actor):
    def __tmp4(__tmp0):
        __tmp0._logger = log.create_logger(logging.INFO, context=PidCacheWatcher)

    async def __tmp5(__tmp0, context) :
        msg = context.message
        if isinstance(msg, Started):
            __tmp0._logger.debug('Started PidCacheWatcher')
        elif isinstance(msg, WatchPidRequest):
            await context.watch(msg.pid)
        elif isinstance(msg, Terminated):
            __typ1().remove_cache_by_pid(msg.who)
