from typing import TypeAlias
__typ0 : TypeAlias = "any"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def schedule_tell_once(__tmp1, __tmp2: timedelta, target, __tmp0: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_tell_repeatedly(__tmp1, __tmp2, interval: timedelta, target, __tmp0: __typ0,
                                       cancellation_token) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_once(__tmp1, __tmp2: timedelta, sender, target,
                                    __tmp0: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_repeatedly(__tmp1, __tmp2: timedelta, interval: timedelta, sender: PID, target: PID,
                                          __tmp0,
                                          cancellation_token: CancelToken) -> None:
        raise NotImplementedError("Should Implement this method")


class SimpleScheduler(AbstractSimpleScheduler):
    def __init__(__tmp1, context: AbstractSenderContext = RootContext()):
        __tmp1._context = context

    async def schedule_tell_once(__tmp1, __tmp2: timedelta, target: PID, __tmp0) :
        async def schedule():
            await asyncio.sleep(__tmp2.total_seconds())
            await __tmp1._context.send(target, __tmp0)

        asyncio.create_task(schedule())

    async def schedule_tell_repeatedly(__tmp1, __tmp2: timedelta, interval: timedelta, target: PID, __tmp0: __typ0,
                                       cancellation_token) -> None:
        async def schedule():
            await cancellation_token.wait(__tmp2.total_seconds())
            while True:
                if cancellation_token.triggered:
                    return
                await __tmp1._context.send(target, __tmp0)
                await cancellation_token.wait(interval.total_seconds())

        asyncio.create_task(schedule())

    async def schedule_request_once(__tmp1, __tmp2: timedelta, sender: <FILL>, target: PID,
                                    __tmp0: __typ0) -> None:
        async def schedule():
            await asyncio.sleep(__tmp2.total_seconds())
            await __tmp1._context.request(target, __tmp0, sender)

        asyncio.create_task(schedule())

    async def schedule_request_repeatedly(__tmp1, __tmp2: timedelta, interval: timedelta, sender: PID, target: PID,
                                          __tmp0, cancellation_token: CancelToken) -> None:
        async def schedule():
            await cancellation_token.cancellable_wait([], timeout=__tmp2.total_seconds())
            while True:
                if cancellation_token.triggered:
                    return
                await __tmp1._context.request(target, __tmp0, sender)
                await cancellation_token.cancellable_wait([], timeout=interval.total_seconds())

        asyncio.create_task(schedule())
