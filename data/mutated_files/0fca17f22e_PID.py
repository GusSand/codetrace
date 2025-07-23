from typing import TypeAlias
__typ3 : TypeAlias = "AbstractMemberStatusEvent"
__typ0 : TypeAlias = "AbstractContext"
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
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


class __typ5(metaclass=Singleton):
    def __tmp2(__tmp1):
        __tmp1._watcher = None
        __tmp1._cluster_topology_evn_sub = None
        __tmp1._cache = {}
        __tmp1._reverse_cache = {}

    async def setup(__tmp1) :
        props = Props.from_producer(lambda: __typ2()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp1._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp1._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp1.process_member_status_event,
                                                                     type(__typ3))

    async def stop(__tmp1) -> None:
        await GlobalRootContext.stop(__tmp1._watcher)
        GlobalEventStream.unsubscribe(__tmp1._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp1, evn) :
        if isinstance(evn, (MemberLeftEvent, MemberRejoinedEvent)):
            __tmp1.remove_cache_by_member_address(evn.address)

    def get_cache(__tmp1, __tmp3) :
        if __tmp3 in __tmp1._cache:
            return __tmp1._cache[__tmp3], True
        return None, False

    async def add_cache(__tmp1, __tmp3, pid) :
        if __tmp3 not in __tmp1._cache:
            key = pid.to_short_string()
            __tmp1._cache[__tmp3] = pid
            __tmp1._reverse_cache[key] = __tmp3

            await GlobalRootContext.send(__tmp1._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp1, pid: <FILL>) :
        key = pid.to_short_string()
        if key in __tmp1._reverse_cache:
            __tmp3 = __tmp1._reverse_cache[key]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp3]

    def remove_cache_by_name(__tmp1, __tmp3) -> None:
        if __tmp3 in __tmp1._cache:
            key = __tmp1._cache[__tmp3]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp3]

    def remove_cache_by_member_address(__tmp1, __tmp0: __typ1) :
        for __tmp3, pid in __tmp1._cache.items():
            if pid.address == __tmp0:
                key = pid.to_short_string()
                del __tmp1._reverse_cache[key]
                del __tmp1._cache[__tmp3]


class __typ2(Actor):
    def __tmp2(__tmp1):
        __tmp1._logger = log.create_logger(logging.INFO, context=__typ2)

    async def receive(__tmp1, context: __typ0) :
        msg = context.message
        if isinstance(msg, Started):
            __tmp1._logger.debug('Started PidCacheWatcher')
        elif isinstance(msg, WatchPidRequest):
            await context.watch(msg.pid)
        elif isinstance(msg, Terminated):
            __typ5().remove_cache_by_pid(msg.who)
