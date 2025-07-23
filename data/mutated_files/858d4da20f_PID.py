from typing import TypeAlias
__typ11 : TypeAlias = "MessageHeader"
__typ9 : TypeAlias = "object"
__typ5 : TypeAlias = "timedelta"
__typ7 : TypeAlias = "Callable"
__typ0 : TypeAlias = "MessageEnvelope"
__typ1 : TypeAlias = "any"
__typ4 : TypeAlias = "str"
__typ10 : TypeAlias = "Task"
__typ6 : TypeAlias = "AbstractRootContext"
__typ3 : TypeAlias = "AbstractContext"
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


class __typ8(__typ6):
    def __tmp4(__tmp1, context: __typ6):
        __tmp1._context = context

    @property
    def headers(__tmp1) -> __typ11:
        return __tmp1._context.headers

    @property
    def message(__tmp1) -> __typ1:
        return __tmp1._context.message

    def spawn(__tmp1, props: 'Props') -> PID:
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp5: __typ4) -> PID:
        return __tmp1._context.spawn_named(props, __tmp5)

    def spawn_prefix(__tmp1, props: 'Props', __tmp3: __typ4) -> PID:
        return __tmp1._context.spawn_prefix(props, __tmp3)

    async def send(__tmp1, __tmp0: PID, message: __typ1) -> None:
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0: PID, message: __typ1, sender: PID = None) -> None:
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0: PID, message: __typ9, timeout: __typ5 = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def stop(__tmp1, __tmp2: PID) -> None:
        await __tmp1._context.stop(__tmp2)

    async def stop_future(__tmp1, __tmp2: PID) -> asyncio.Future:
        return await __tmp1._context.stop_future(__tmp2)

    async def poison(__tmp1, __tmp2: PID) -> None:
        await __tmp1._context.poison(__tmp2)

    async def poison_future(__tmp1, __tmp2: PID) -> asyncio.Future:
        return await __tmp1._context.poison_future(__tmp2)


class __typ2(__typ3):
    def __tmp4(__tmp1, context: __typ3):
        __tmp1._context = context

    @property
    def headers(__tmp1) -> __typ11:
        return __tmp1._context.headers

    @property
    def message(__tmp1) -> __typ1:
        return __tmp1._context.message

    @property
    def parent(__tmp1) -> PID:
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
    def receive_timeout(__tmp1) -> __typ5:
        return __tmp1._context.receive_timeout

    @property
    def children(__tmp1):
        return __tmp1._context.children

    @property
    def stash(__tmp1):
        return __tmp1._context.stash

    async def send(__tmp1, __tmp0: PID, message: __typ1) -> None:
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0, message: __typ1, sender: PID = None) -> None:
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0: PID, message: __typ9, timeout: __typ5 = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def receive(__tmp1, envelope: __typ0):
        return await __tmp1._context.receive(envelope)

    async def respond(__tmp1, message: __typ9):
        return await __tmp1._context.respond(message)

    def spawn(__tmp1, props: 'Props') -> PID:
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp5) -> PID:
        return __tmp1._context.spawn_named(props, __tmp5)

    def spawn_prefix(__tmp1, props: 'Props', __tmp3: __typ4) -> PID:
        return __tmp1._context.spawn_prefix(props, __tmp3)

    async def watch(__tmp1, __tmp2: <FILL>) -> None:
        await __tmp1._context.watch(__tmp2)

    async def unwatch(__tmp1, __tmp2: PID) -> None:
        await __tmp1._context.unwatch(__tmp2)

    def set_receive_timeout(__tmp1, receive_timeout: __typ5) -> None:
        __tmp1._context.set_receive_timeout(receive_timeout)

    def cancel_receive_timeout(__tmp1) -> None:
        __tmp1._context.cancel_receive_timeout()

    async def forward(__tmp1, __tmp0: PID) -> None:
        await __tmp1._context.forward(__tmp0)

    def reenter_after(__tmp1, __tmp0: __typ10, action: __typ7) :
        __tmp1._context.reenter_after(__tmp0, action)

    async def stop(__tmp1, __tmp2: PID) -> None:
        pass

    async def stop_future(__tmp1, __tmp2) -> Future:
        pass

    async def poison(__tmp1, __tmp2: PID) -> None:
        pass

    async def poison_future(__tmp1, __tmp2: PID) -> Future:
        pass
