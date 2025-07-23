from typing import TypeAlias
__typ0 : TypeAlias = "AbstractMemberStatusValue"
import asyncio
from datetime import timedelta
from typing import List

from protoactor.actor.actor_context import AbstractContext, GlobalRootContext
from protoactor.actor.event_stream import GlobalEventStream
from protoactor.actor.props import Props
from protoactor.mailbox.dispatcher import Dispatchers
from protoactor.remote.remote import Remote
from protoactor.remote.serialization import Serialization
from protoactor.cluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer, \
    MemberStatus
from protoactor.cluster.member_status_events import ClusterTopologyEvent
from protoactor.cluster.providers.abstract_cluster_provider import AbstractClusterProvider
from protoactor.cluster.providers.single_remote_instance.protos_pb2 import GetKinds, GetKindsResponse, DESCRIPTOR


class SingleRemoteInstanceProvider(AbstractClusterProvider):
    def __init__(__tmp1, server_host: <FILL>, __tmp4):
        __tmp1._kinds_responder = 'remote_kinds_responder'
        __tmp1._timeout = timedelta(seconds=10)

        __tmp1._server_host = server_host
        __tmp1._server_port = __tmp4
        __tmp1._server_address = '%s:%s' % (server_host, str(__tmp4))

        __tmp1._kinds = []
        __tmp1._ok_status = None
        __tmp1._ko_status = None

        __tmp1._is_server = None
        __tmp1._shutdown = None

        async def __tmp5(__tmp8: AbstractContext):
            if isinstance(__tmp8.message, GetKinds) and __tmp8.sender is not None:
                await __tmp8.respond(GetKindsResponse(kinds=__tmp1._kinds))

        props = Props.from_func(__tmp5)

        Serialization().register_file_descriptor(DESCRIPTOR)
        Remote().register_known_kind(__tmp1._kinds_responder, props)

    async def register_member_async(__tmp1, __tmp2: str, host: str, port: int, kinds,
                                    status_value: __typ0,
                                    serializer: AbstractMemberStatusValueSerializer) -> None:
        __tmp1._kinds = kinds
        __tmp1._ok_status = serializer.from_value_bytes('Ok!'.encode())
        __tmp1._ko_status = serializer.from_value_bytes('Ko!'.encode())

        __tmp1._is_server = host == __tmp1._server_host and port == __tmp1._server_port

    async def __tmp0(__tmp1) :
        pass

    def __tmp7(__tmp1) :
        async def __tmp5():
            while not __tmp1._shutdown:
                await __tmp1.__notify_statuses()

        Dispatchers().default_dispatcher.schedule(__tmp5)

    async def __tmp3(__tmp1, status_value) -> None:
        pass

    def __tmp6(__tmp1) -> None:
        __tmp1._shutdown = True

    async def __notify_statuses(__tmp1):
        status = None
        if __tmp1._is_server:
            status = MemberStatus(__tmp1._server_address, __tmp1._server_host, __tmp1._server_port, __tmp1._kinds, True,
                                  __tmp1._ok_status)
        else:
            responder = await Remote().spawn_named_async(__tmp1._server_address, __tmp1._kinds_responder,
                                                         __tmp1._kinds_responder, __tmp1._timeout)
            if responder.pid is not None:
                try:
                    response = await GlobalRootContext.request_future(responder.pid, GetKinds(), __tmp1._timeout)
                    status = MemberStatus(__tmp1._server_address, __tmp1._server_host, __tmp1._server_port, response.kinds,
                                          True, __tmp1._ok_status)
                except TimeoutError:
                    status = MemberStatus(__tmp1._server_address, __tmp1._server_host, __tmp1._server_port, [], True,
                                          __tmp1._ko_status)
            else:
                status = MemberStatus(__tmp1._server_address, __tmp1._server_host, __tmp1._server_port, [], False,
                                      __tmp1._ko_status)

        event = ClusterTopologyEvent([status])
        await GlobalEventStream.publish(event)
        await asyncio.sleep(60)