from typing import TypeAlias
__typ1 : TypeAlias = "AbstractRootContext"
__typ4 : TypeAlias = "Task"
__typ0 : TypeAlias = "any"
__typ3 : TypeAlias = "object"
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


class __typ2(__typ1):
    def __init__(__tmp2, context: __typ1):
        __tmp2._context = context

    @property
    def headers(__tmp2) -> MessageHeader:
        return __tmp2._context.headers

    @property
    def message(__tmp2) -> __typ0:
        return __tmp2._context.message

    def spawn(__tmp2, props: 'Props') -> PID:
        return __tmp2._context.spawn(props)

    def spawn_named(__tmp2, props, name: str) -> PID:
        return __tmp2._context.spawn_named(props, name)

    def spawn_prefix(__tmp2, props: 'Props', prefix: str) -> PID:
        return __tmp2._context.spawn_prefix(props, prefix)

    async def send(__tmp2, __tmp1: PID, message: __typ0) -> None:
        await __tmp2._context.send(__tmp1, message)

    async def request(__tmp2, __tmp1: PID, message: __typ0, sender: PID = None) -> None:
        await __tmp2._context.request(__tmp1, message, sender)

    async def request_future(__tmp2, __tmp1, message, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp2._context.request_future(__tmp1, message, timeout, cancellation_token)

    async def stop(__tmp2, __tmp0: PID) -> None:
        await __tmp2._context.stop(__tmp0)

    async def stop_future(__tmp2, __tmp0) -> asyncio.Future:
        return await __tmp2._context.stop_future(__tmp0)

    async def poison(__tmp2, __tmp0: PID) -> None:
        await __tmp2._context.poison(__tmp0)

    async def poison_future(__tmp2, __tmp0) -> asyncio.Future:
        return await __tmp2._context.poison_future(__tmp0)


class ActorContextDecorator(AbstractContext):
    def __init__(__tmp2, context: AbstractContext):
        __tmp2._context = context

    @property
    def headers(__tmp2) -> MessageHeader:
        return __tmp2._context.headers

    @property
    def message(__tmp2) -> __typ0:
        return __tmp2._context.message

    @property
    def parent(__tmp2) -> PID:
        return __tmp2._context.parent

    @property
    def my_self(__tmp2) -> PID:
        return __tmp2._context.my_self

    @property
    def sender(__tmp2) -> PID:
        return __tmp2._context.sender

    @property
    def actor(__tmp2) -> 'Actor':
        return __tmp2._context.actor

    @property
    def receive_timeout(__tmp2) -> timedelta:
        return __tmp2._context.receive_timeout

    @property
    def children(__tmp2):
        return __tmp2._context.children

    @property
    def stash(__tmp2):
        return __tmp2._context.stash

    async def send(__tmp2, __tmp1: PID, message: __typ0) -> None:
        await __tmp2._context.send(__tmp1, message)

    async def request(__tmp2, __tmp1: PID, message: __typ0, sender: PID = None) -> None:
        await __tmp2._context.request(__tmp1, message, sender)

    async def request_future(__tmp2, __tmp1: <FILL>, message: __typ3, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp2._context.request_future(__tmp1, message, timeout, cancellation_token)

    async def receive(__tmp2, envelope: MessageEnvelope):
        return await __tmp2._context.receive(envelope)

    async def respond(__tmp2, message: __typ3):
        return await __tmp2._context.respond(message)

    def spawn(__tmp2, props: 'Props') -> PID:
        return __tmp2._context.spawn(props)

    def spawn_named(__tmp2, props: 'Props', name: str) -> PID:
        return __tmp2._context.spawn_named(props, name)

    def spawn_prefix(__tmp2, props: 'Props', prefix: str) :
        return __tmp2._context.spawn_prefix(props, prefix)

    async def watch(__tmp2, __tmp0: PID) -> None:
        await __tmp2._context.watch(__tmp0)

    async def unwatch(__tmp2, __tmp0: PID) -> None:
        await __tmp2._context.unwatch(__tmp0)

    def set_receive_timeout(__tmp2, receive_timeout: timedelta) -> None:
        __tmp2._context.set_receive_timeout(receive_timeout)

    def cancel_receive_timeout(__tmp2) -> None:
        __tmp2._context.cancel_receive_timeout()

    async def forward(__tmp2, __tmp1: PID) -> None:
        await __tmp2._context.forward(__tmp1)

    def reenter_after(__tmp2, __tmp1: __typ4, action: Callable) -> None:
        __tmp2._context.reenter_after(__tmp1, action)

    async def stop(__tmp2, __tmp0: PID) -> None:
        pass

    async def stop_future(__tmp2, __tmp0: PID) -> Future:
        pass

    async def poison(__tmp2, __tmp0: PID) -> None:
        pass

    async def poison_future(__tmp2, __tmp0: PID) -> Future:
        pass
