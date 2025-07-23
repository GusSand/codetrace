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
    def __tmp2(__tmp1):
        __tmp1._watcher = None
        __tmp1._cluster_topology_evn_sub = None
        __tmp1._cache = {}
        __tmp1._reverse_cache = {}

    async def setup(__tmp1) -> None:
        props = Props.from_producer(lambda: PidCacheWatcher()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp1._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp1._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp1.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp1) :
        await GlobalRootContext.stop(__tmp1._watcher)
        GlobalEventStream.unsubscribe(__tmp1._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp1, evn: AbstractMemberStatusEvent) -> None:
        if isinstance(evn, MemberLeftEvent) or isinstance(evn, MemberRejoinedEvent):
            __tmp1.remove_cache_by_member_address(evn.address)

    def get_cache(__tmp1, __tmp3: str) -> Tuple[PID, bool]:
        if __tmp3 in __tmp1._cache.keys():
            return __tmp1._cache[__tmp3], True
        else:
            return None, False

    async def add_cache(__tmp1, __tmp3: <FILL>, pid: PID) -> bool:
        if __tmp3 not in __tmp1._cache.keys():
            key = pid.to_short_string()
            __tmp1._cache[__tmp3] = pid
            __tmp1._reverse_cache[key] = __tmp3

            await GlobalRootContext.send(__tmp1._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp1, pid) -> None:
        key = pid.to_short_string()
        if key in __tmp1._reverse_cache:
            __tmp3 = __tmp1._reverse_cache[key]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp3]

    def __tmp0(__tmp1, __tmp3: str) :
        if __tmp3 in __tmp1._cache:
            key = __tmp1._cache[__tmp3]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp3]

    def remove_cache_by_member_address(__tmp1, member_address) :
        for __tmp3, pid in __tmp1._cache.items():
            if pid.address == member_address:
                key = pid.to_short_string()
                del __tmp1._reverse_cache[key]
                del __tmp1._cache[__tmp3]


class PidCacheWatcher(Actor):
    def __tmp2(__tmp1):
        __tmp1._logger = None

    async def receive(__tmp1, context) :
        msg = context.message
        if isinstance(msg, Started):
            # self._logger.log_debug('Started PidCacheWatcher')
            pass
        elif isinstance(msg, WatchPidRequest):
            await context.watch(msg.pid)
        elif isinstance(msg, Terminated):
            PidCache().remove_cache_by_pid(msg.who)
