from typing import TypeAlias
__typ1 : TypeAlias = "any"
__typ0 : TypeAlias = "Task"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "timedelta"
import asyncio
from asyncio.futures import Future
from asyncio.tasks import Task
from datetime import timedelta
from typing import Callable

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractRootContext, AbstractContext
from protoactor.actor.cancel_token import CancelToken
from protoactor.actor.message_envelope import MessageEnvelope
from protoactor.actor.message_header import MessageHeader
from protoactor.actor.props import Props

is_import = False
if is_import:
    from protoactor.actor.actor import Actor


class RootContextDecorator(AbstractRootContext):
    def __init__(__tmp1, context: AbstractRootContext):
        __tmp1._context = context

    @property
    def headers(__tmp1) -> MessageHeader:
        return __tmp1._context.headers

    @property
    def message(__tmp1) -> __typ1:
        return __tmp1._context.message

    def spawn(__tmp1, props) -> PID:
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp2: __typ2) -> PID:
        return __tmp1._context.spawn_named(props, __tmp2)

    def spawn_prefix(__tmp1, props: 'Props', prefix: __typ2) -> PID:
        return __tmp1._context.spawn_prefix(props, prefix)

    async def send(__tmp1, __tmp0: PID, message: __typ1) -> None:
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0: PID, message: __typ1, sender: PID = None) -> None:
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0: PID, message: object, timeout: __typ3 = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def stop(__tmp1, pid: PID) -> None:
        await __tmp1._context.stop(pid)

    async def stop_future(__tmp1, pid) -> asyncio.Future:
        return await __tmp1._context.stop_future(pid)

    async def poison(__tmp1, pid: PID) -> None:
        await __tmp1._context.poison(pid)

    async def poison_future(__tmp1, pid: PID) :
        return await __tmp1._context.poison_future(pid)


class ActorContextDecorator(AbstractContext):
    def __init__(__tmp1, context: AbstractContext):
        __tmp1._context = context

    @property
    def headers(__tmp1) -> MessageHeader:
        return __tmp1._context.headers

    @property
    def message(__tmp1) -> __typ1:
        return __tmp1._context.message

    @property
    def parent(__tmp1) :
        return __tmp1._context.parent

    @property
    def my_self(__tmp1) -> PID:
        return __tmp1._context.my_self

    @property
    def sender(__tmp1) -> PID:
        return __tmp1._context.sender

    @property
    def actor(__tmp1) -> 'Actor':
        return __tmp1._context.actor

    @property
    def receive_timeout(__tmp1) -> __typ3:
        return __tmp1._context.receive_timeout

    @property
    def children(__tmp1):
        return __tmp1._context.children

    @property
    def stash(__tmp1):
        return __tmp1._context.stash

    async def send(__tmp1, __tmp0: PID, message: __typ1) -> None:
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0: PID, message, sender: PID = None) -> None:
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0, message, timeout: __typ3 = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def receive(__tmp1, envelope: MessageEnvelope):
        return await __tmp1._context.receive(envelope)

    async def respond(__tmp1, message: object):
        return await __tmp1._context.respond(message)

    def spawn(__tmp1, props: 'Props') :
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props, __tmp2: __typ2) -> PID:
        return __tmp1._context.spawn_named(props, __tmp2)

    def spawn_prefix(__tmp1, props: 'Props', prefix) -> PID:
        return __tmp1._context.spawn_prefix(props, prefix)

    async def watch(__tmp1, pid: PID) -> None:
        await __tmp1._context.watch(pid)

    async def unwatch(__tmp1, pid: PID) -> None:
        await __tmp1._context.unwatch(pid)

    def set_receive_timeout(__tmp1, receive_timeout: __typ3) -> None:
        __tmp1._context.set_receive_timeout(receive_timeout)

    def cancel_receive_timeout(__tmp1) -> None:
        __tmp1._context.cancel_receive_timeout()

    async def forward(__tmp1, __tmp0: <FILL>) -> None:
        await __tmp1._context.forward(__tmp0)

    def reenter_after(__tmp1, __tmp0: __typ0, action: Callable) -> None:
        __tmp1._context.reenter_after(__tmp0, action)

    async def stop(__tmp1, pid: PID) -> None:
        pass

    async def stop_future(__tmp1, pid) -> Future:
        pass

    async def poison(__tmp1, pid: PID) -> None:
        pass

    async def poison_future(__tmp1, pid: PID) -> Future:
        pass
