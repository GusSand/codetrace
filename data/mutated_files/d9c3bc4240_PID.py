from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "object"
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
    def __tmp4(__tmp1, context):
        __tmp1._context = context

    @property
    def headers(__tmp1) -> MessageHeader:
        return __tmp1._context.headers

    @property
    def message(__tmp1) :
        return __tmp1._context.message

    def spawn(__tmp1, props) :
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp6) -> PID:
        return __tmp1._context.spawn_named(props, __tmp6)

    def spawn_prefix(__tmp1, props, __tmp5) -> PID:
        return __tmp1._context.spawn_prefix(props, __tmp5)

    async def send(__tmp1, __tmp0, message) -> None:
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0: PID, message, sender: PID = None) :
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0: PID, message, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) :
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def stop(__tmp1, __tmp2: PID) -> None:
        await __tmp1._context.stop(__tmp2)

    async def stop_future(__tmp1, __tmp2: PID) -> asyncio.Future:
        return await __tmp1._context.stop_future(__tmp2)

    async def poison(__tmp1, __tmp2) -> None:
        await __tmp1._context.poison(__tmp2)

    async def poison_future(__tmp1, __tmp2: PID) :
        return await __tmp1._context.poison_future(__tmp2)


class ActorContextDecorator(AbstractContext):
    def __tmp4(__tmp1, context: AbstractContext):
        __tmp1._context = context

    @property
    def headers(__tmp1) :
        return __tmp1._context.headers

    @property
    def message(__tmp1) :
        return __tmp1._context.message

    @property
    def parent(__tmp1) :
        return __tmp1._context.parent

    @property
    def my_self(__tmp1) :
        return __tmp1._context.my_self

    @property
    def sender(__tmp1) -> PID:
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

    async def send(__tmp1, __tmp0: PID, message) -> None:
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0, message: __typ0, sender: PID = None) -> None:
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0, message, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def receive(__tmp1, envelope):
        return await __tmp1._context.receive(envelope)

    async def respond(__tmp1, message: __typ1):
        return await __tmp1._context.respond(message)

    def spawn(__tmp1, props: 'Props') :
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp6) -> PID:
        return __tmp1._context.spawn_named(props, __tmp6)

    def spawn_prefix(__tmp1, props: 'Props', __tmp5: str) :
        return __tmp1._context.spawn_prefix(props, __tmp5)

    async def watch(__tmp1, __tmp2: PID) -> None:
        await __tmp1._context.watch(__tmp2)

    async def unwatch(__tmp1, __tmp2) -> None:
        await __tmp1._context.unwatch(__tmp2)

    def set_receive_timeout(__tmp1, receive_timeout) -> None:
        __tmp1._context.set_receive_timeout(receive_timeout)

    def cancel_receive_timeout(__tmp1) :
        __tmp1._context.cancel_receive_timeout()

    async def forward(__tmp1, __tmp0) -> None:
        await __tmp1._context.forward(__tmp0)

    def reenter_after(__tmp1, __tmp0: Task, __tmp3: Callable) :
        __tmp1._context.reenter_after(__tmp0, __tmp3)

    async def stop(__tmp1, __tmp2: <FILL>) :
        pass

    async def stop_future(__tmp1, __tmp2: PID) :
        pass

    async def poison(__tmp1, __tmp2: PID) :
        pass

    async def poison_future(__tmp1, __tmp2: PID) :
        pass
