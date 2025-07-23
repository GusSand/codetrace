from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
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


class __typ3(metaclass=Singleton):
    def __tmp6(__tmp1):
        __tmp1._watcher = None
        __tmp1._cluster_topology_evn_sub = None
        __tmp1._cache = {}
        __tmp1._reverse_cache = {}

    async def setup(__tmp1) -> None:
        props = Props.from_producer(lambda: __typ2()) \
            .with_guardian_supervisor_strategy(Supervision.always_restart_strategy)

        __tmp1._watcher = GlobalRootContext.spawn_named(props, 'PidCacheWatcher')
        __tmp1._cluster_topology_evn_sub = GlobalEventStream.subscribe(__tmp1.process_member_status_event,
                                                                     type(AbstractMemberStatusEvent))

    async def stop(__tmp1) -> None:
        await GlobalRootContext.stop(__tmp1._watcher)
        GlobalEventStream.unsubscribe(__tmp1._cluster_topology_evn_sub.id)

    def process_member_status_event(__tmp1, __tmp3: AbstractMemberStatusEvent) :
        if isinstance(__tmp3, MemberLeftEvent) or isinstance(__tmp3, MemberRejoinedEvent):
            __tmp1.remove_cache_by_member_address(__tmp3.address)

    def __tmp2(__tmp1, __tmp7: __typ0) :
        if __tmp7 in __tmp1._cache.keys():
            return __tmp1._cache[__tmp7], True
        else:
            return None, False

    async def add_cache(__tmp1, __tmp7: __typ0, pid: <FILL>) -> __typ1:
        if __tmp7 not in __tmp1._cache.keys():
            key = pid.to_short_string()
            __tmp1._cache[__tmp7] = pid
            __tmp1._reverse_cache[key] = __tmp7

            await GlobalRootContext.send(__tmp1._watcher, WatchPidRequest(pid))
            return True
        return False

    def remove_cache_by_pid(__tmp1, pid: PID) -> None:
        key = pid.to_short_string()
        if key in __tmp1._reverse_cache:
            __tmp7 = __tmp1._reverse_cache[key]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp7]

    def __tmp4(__tmp1, __tmp7: __typ0) -> None:
        if __tmp7 in __tmp1._cache:
            key = __tmp1._cache[__tmp7]
            del __tmp1._reverse_cache[key]
            del __tmp1._cache[__tmp7]

    def remove_cache_by_member_address(__tmp1, __tmp5: __typ0) -> None:
        for __tmp7, pid in __tmp1._cache.items():
            if pid.address == __tmp5:
                key = pid.to_short_string()
                del __tmp1._reverse_cache[key]
                del __tmp1._cache[__tmp7]


class __typ2(Actor):
    def __tmp6(__tmp1):
        __tmp1._logger = None

    async def receive(__tmp1, __tmp0: AbstractContext) :
        msg = __tmp0.message
        if isinstance(msg, Started):
            # self._logger.log_debug('Started PidCacheWatcher')
            pass
        elif isinstance(msg, WatchPidRequest):
            await __tmp0.watch(msg.pid)
        elif isinstance(msg, Terminated):
            __typ3().remove_cache_by_pid(msg.who)
