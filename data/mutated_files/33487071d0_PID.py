from typing import TypeAlias
__typ8 : TypeAlias = "Task"
__typ0 : TypeAlias = "MessageEnvelope"
__typ3 : TypeAlias = "timedelta"
__typ1 : TypeAlias = "any"
__typ5 : TypeAlias = "AbstractRootContext"
__typ6 : TypeAlias = "Callable"
__typ7 : TypeAlias = "object"
__typ4 : TypeAlias = "str"
__typ9 : TypeAlias = "MessageHeader"
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


class RootContextDecorator(__typ5):
    def __init__(__tmp1, context):
        __tmp1._context = context

    @property
    def headers(__tmp1) :
        return __tmp1._context.headers

    @property
    def message(__tmp1) :
        return __tmp1._context.message

    def spawn(__tmp1, props) :
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props, name) :
        return __tmp1._context.spawn_named(props, name)

    def spawn_prefix(__tmp1, props, prefix: __typ4) :
        return __tmp1._context.spawn_prefix(props, prefix)

    async def send(__tmp1, target: <FILL>, message) :
        await __tmp1._context.send(target, message)

    async def request(__tmp1, target, message, sender: PID = None) :
        await __tmp1._context.request(target, message, sender)

    async def request_future(__tmp1, target: PID, message: __typ7, timeout: __typ3 = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(target, message, timeout, cancellation_token)

    async def stop(__tmp1, __tmp0: PID) -> None:
        await __tmp1._context.stop(__tmp0)

    async def stop_future(__tmp1, __tmp0: PID) -> asyncio.Future:
        return await __tmp1._context.stop_future(__tmp0)

    async def poison(__tmp1, __tmp0) -> None:
        await __tmp1._context.poison(__tmp0)

    async def poison_future(__tmp1, __tmp0) -> asyncio.Future:
        return await __tmp1._context.poison_future(__tmp0)


class __typ2(AbstractContext):
    def __init__(__tmp1, context):
        __tmp1._context = context

    @property
    def headers(__tmp1) :
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
    def sender(__tmp1) :
        return __tmp1._context.sender

    @property
    def actor(__tmp1) -> 'Actor':
        return __tmp1._context.actor

    @property
    def receive_timeout(__tmp1) :
        return __tmp1._context.receive_timeout

    @property
    def children(__tmp1):
        return __tmp1._context.children

    @property
    def stash(__tmp1):
        return __tmp1._context.stash

    async def send(__tmp1, target, message) :
        await __tmp1._context.send(target, message)

    async def request(__tmp1, target, message, sender: PID = None) -> None:
        await __tmp1._context.request(target, message, sender)

    async def request_future(__tmp1, target, message, timeout: __typ3 = None,
                             cancellation_token: CancelToken = None) :
        return await __tmp1._context.request_future(target, message, timeout, cancellation_token)

    async def receive(__tmp1, envelope: __typ0):
        return await __tmp1._context.receive(envelope)

    async def respond(__tmp1, message: __typ7):
        return await __tmp1._context.respond(message)

    def spawn(__tmp1, props) :
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', name) :
        return __tmp1._context.spawn_named(props, name)

    def spawn_prefix(__tmp1, props: 'Props', prefix) -> PID:
        return __tmp1._context.spawn_prefix(props, prefix)

    async def watch(__tmp1, __tmp0) :
        await __tmp1._context.watch(__tmp0)

    async def unwatch(__tmp1, __tmp0) :
        await __tmp1._context.unwatch(__tmp0)

    def set_receive_timeout(__tmp1, receive_timeout: __typ3) -> None:
        __tmp1._context.set_receive_timeout(receive_timeout)

    def cancel_receive_timeout(__tmp1) :
        __tmp1._context.cancel_receive_timeout()

    async def forward(__tmp1, target: PID) :
        await __tmp1._context.forward(target)

    def reenter_after(__tmp1, target: __typ8, action) :
        __tmp1._context.reenter_after(target, action)

    async def stop(__tmp1, __tmp0: PID) -> None:
        pass

    async def stop_future(__tmp1, __tmp0) -> Future:
        pass

    async def poison(__tmp1, __tmp0) -> None:
        pass

    async def poison_future(__tmp1, __tmp0: PID) :
        pass
