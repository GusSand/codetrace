from typing import TypeAlias
__typ2 : TypeAlias = "CancelToken"
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "PID"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class __typ4(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp6(__tmp2, __tmp12, __tmp1: __typ1, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp2, __tmp12: timedelta, __tmp4, __tmp1: __typ1, __tmp0,
                                       __tmp10: __typ2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp2, __tmp12: timedelta, __tmp3: __typ1, __tmp1,
                                    __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp11(__tmp2, __tmp12: timedelta, __tmp4: timedelta, __tmp3: __typ1, __tmp1: __typ1,
                                          __tmp0,
                                          __tmp10: __typ2) :
        raise NotImplementedError("Should Implement this method")


class __typ3(__typ4):
    def __tmp9(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp6(__tmp2, __tmp12: timedelta, __tmp1, __tmp0) :
        async def __tmp8():
            await asyncio.sleep(__tmp12.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp8())

    async def __tmp7(__tmp2, __tmp12: timedelta, __tmp4: timedelta, __tmp1: __typ1, __tmp0,
                                       __tmp10) -> None:
        async def __tmp8():
            await __tmp10.wait(__tmp12.total_seconds())
            while True:
                if __tmp10.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp10.wait(__tmp4.total_seconds())

        asyncio.create_task(__tmp8())

    async def __tmp5(__tmp2, __tmp12, __tmp3, __tmp1,
                                    __tmp0) -> None:
        async def __tmp8():
            await asyncio.sleep(__tmp12.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp3)

        asyncio.create_task(__tmp8())

    async def __tmp11(__tmp2, __tmp12: <FILL>, __tmp4, __tmp3: __typ1, __tmp1,
                                          __tmp0: __typ0, __tmp10) -> None:
        async def __tmp8():
            await __tmp10.cancellable_wait([], timeout=__tmp12.total_seconds())
            while True:
                if __tmp10.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp3)
                await __tmp10.cancellable_wait([], timeout=__tmp4.total_seconds())

        asyncio.create_task(__tmp8())
