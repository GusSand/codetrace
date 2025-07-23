from typing import TypeAlias
__typ3 : TypeAlias = "PID"
__typ0 : TypeAlias = "MessageEnvelope"
__typ1 : TypeAlias = "any"
__typ7 : TypeAlias = "object"
__typ8 : TypeAlias = "MessageHeader"
__typ5 : TypeAlias = "Callable"
__typ4 : TypeAlias = "timedelta"
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


class __typ6(AbstractRootContext):
    def __tmp4(__tmp1, context):
        __tmp1._context = context

    @property
    def headers(__tmp1) :
        return __tmp1._context.headers

    @property
    def message(__tmp1) :
        return __tmp1._context.message

    def spawn(__tmp1, props) -> __typ3:
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp6) :
        return __tmp1._context.spawn_named(props, __tmp6)

    def spawn_prefix(__tmp1, props: 'Props', __tmp5: str) :
        return __tmp1._context.spawn_prefix(props, __tmp5)

    async def send(__tmp1, __tmp0, message) :
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0, message, sender: __typ3 = None) :
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0, message: __typ7, timeout: __typ4 = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def stop(__tmp1, __tmp2: __typ3) -> None:
        await __tmp1._context.stop(__tmp2)

    async def stop_future(__tmp1, __tmp2) :
        return await __tmp1._context.stop_future(__tmp2)

    async def poison(__tmp1, __tmp2) :
        await __tmp1._context.poison(__tmp2)

    async def poison_future(__tmp1, __tmp2: __typ3) -> asyncio.Future:
        return await __tmp1._context.poison_future(__tmp2)


class __typ2(AbstractContext):
    def __tmp4(__tmp1, context: AbstractContext):
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
    def my_self(__tmp1) -> __typ3:
        return __tmp1._context.my_self

    @property
    def sender(__tmp1) -> __typ3:
        return __tmp1._context.sender

    @property
    def actor(__tmp1) :
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

    async def send(__tmp1, __tmp0, message: __typ1) :
        await __tmp1._context.send(__tmp0, message)

    async def request(__tmp1, __tmp0: __typ3, message, sender: __typ3 = None) -> None:
        await __tmp1._context.request(__tmp0, message, sender)

    async def request_future(__tmp1, __tmp0, message, timeout: __typ4 = None,
                             cancellation_token: CancelToken = None) :
        return await __tmp1._context.request_future(__tmp0, message, timeout, cancellation_token)

    async def receive(__tmp1, envelope):
        return await __tmp1._context.receive(envelope)

    async def respond(__tmp1, message):
        return await __tmp1._context.respond(message)

    def spawn(__tmp1, props) -> __typ3:
        return __tmp1._context.spawn(props)

    def spawn_named(__tmp1, props: 'Props', __tmp6: <FILL>) :
        return __tmp1._context.spawn_named(props, __tmp6)

    def spawn_prefix(__tmp1, props: 'Props', __tmp5) :
        return __tmp1._context.spawn_prefix(props, __tmp5)

    async def watch(__tmp1, __tmp2) :
        await __tmp1._context.watch(__tmp2)

    async def unwatch(__tmp1, __tmp2) :
        await __tmp1._context.unwatch(__tmp2)

    def set_receive_timeout(__tmp1, receive_timeout: __typ4) :
        __tmp1._context.set_receive_timeout(receive_timeout)

    def cancel_receive_timeout(__tmp1) :
        __tmp1._context.cancel_receive_timeout()

    async def forward(__tmp1, __tmp0: __typ3) :
        await __tmp1._context.forward(__tmp0)

    def reenter_after(__tmp1, __tmp0, __tmp3) :
        __tmp1._context.reenter_after(__tmp0, __tmp3)

    async def stop(__tmp1, __tmp2) :
        pass

    async def stop_future(__tmp1, __tmp2) :
        pass

    async def poison(__tmp1, __tmp2) :
        pass

    async def poison_future(__tmp1, __tmp2: __typ3) :
        pass
