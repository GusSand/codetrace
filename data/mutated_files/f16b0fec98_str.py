from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "PID"
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
    def __init__(__tmp0):
        __tmp0._watcher = None
        __tmp0._cluster_topology_evn_sub = None
        __tmp0._cache = {}
        __tmp0._reverse_cache = {}

    async def setup(__tmp0) -> None:
        props = Props.from_producer(lambda: PidCacheWatcher()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp0._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp0._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp0.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp0) :
        await GlobalRootContext.stop(__tmp0._watcher)
        GlobalEventStream.unsubscribe(__tmp0._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp0, evn) -> None:
        if isinstance(evn, (MemberLeftEvent, MemberRejoinedEvent)):
            __tmp0.remove_cache_by_member_address(evn.address)

    def get_cache(__tmp0, name) :
        if name in __tmp0._cache:
            return __tmp0._cache[name], True
        return None, False

    async def add_cache(__tmp0, name: str, pid: __typ0) -> __typ2:
        if name not in __tmp0._cache:
            key = pid.to_short_string()
            __tmp0._cache[name] = pid
            __tmp0._reverse_cache[key] = name

            await GlobalRootContext.send(__tmp0._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp0, pid) :
        key = pid.to_short_string()
        if key in __tmp0._reverse_cache:
            name = __tmp0._reverse_cache[key]
            del __tmp0._reverse_cache[key]
            del __tmp0._cache[name]

    def remove_cache_by_name(__tmp0, name) :
        if name in __tmp0._cache:
            key = __tmp0._cache[name]
            del __tmp0._reverse_cache[key]
            del __tmp0._cache[name]

    def remove_cache_by_member_address(__tmp0, member_address: <FILL>) -> None:
        for name, pid in __tmp0._cache.items():
            if pid.address == member_address:
                key = pid.to_short_string()
                del __tmp0._reverse_cache[key]
                del __tmp0._cache[name]


class PidCacheWatcher(Actor):
    def __init__(__tmp0):
        __tmp0._logger = log.create_logger(logging.INFO, context=PidCacheWatcher)

    async def receive(__tmp0, context: AbstractContext) -> None:
        msg = context.message
        if isinstance(msg, Started):
            __tmp0._logger.debug('Started PidCacheWatcher')
        elif isinstance(msg, WatchPidRequest):
            await context.watch(msg.pid)
        elif isinstance(msg, Terminated):
            __typ1().remove_cache_by_pid(msg.who)
