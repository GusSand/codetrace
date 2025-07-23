from typing import TypeAlias
__typ2 : TypeAlias = "timedelta"
__typ1 : TypeAlias = "CancelToken"
__typ0 : TypeAlias = "any"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class __typ4(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp3(__tmp1, __tmp10: __typ2, __tmp0: PID, message: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_tell_repeatedly(__tmp1, __tmp10: __typ2, __tmp4: __typ2, __tmp0: PID, message: __typ0,
                                       __tmp8: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp1, __tmp10: __typ2, __tmp2: <FILL>, __tmp0: PID,
                                    message: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp9(__tmp1, __tmp10: __typ2, __tmp4: __typ2, __tmp2: PID, __tmp0: PID,
                                          message: __typ0,
                                          __tmp8: __typ1) :
        raise NotImplementedError("Should Implement this method")


class __typ3(__typ4):
    def __tmp7(__tmp1, context: AbstractSenderContext = RootContext()):
        __tmp1._context = context

    async def __tmp3(__tmp1, __tmp10: __typ2, __tmp0: PID, message: __typ0) -> None:
        async def __tmp6():
            await asyncio.sleep(__tmp10.total_seconds())
            await __tmp1._context.send(__tmp0, message)

        asyncio.create_task(__tmp6())

    async def schedule_tell_repeatedly(__tmp1, __tmp10: __typ2, __tmp4: __typ2, __tmp0: PID, message,
                                       __tmp8: __typ1) :
        async def __tmp6():
            await __tmp8.wait(__tmp10.total_seconds())
            while True:
                if __tmp8.triggered:
                    return
                await __tmp1._context.send(__tmp0, message)
                await __tmp8.wait(__tmp4.total_seconds())

        asyncio.create_task(__tmp6())

    async def __tmp5(__tmp1, __tmp10: __typ2, __tmp2: PID, __tmp0: PID,
                                    message) :
        async def __tmp6():
            await asyncio.sleep(__tmp10.total_seconds())
            await __tmp1._context.request(__tmp0, message, __tmp2)

        asyncio.create_task(__tmp6())

    async def __tmp9(__tmp1, __tmp10, __tmp4, __tmp2: PID, __tmp0: PID,
                                          message: __typ0, __tmp8: __typ1) -> None:
        async def __tmp6():
            await __tmp8.cancellable_wait([], timeout=__tmp10.total_seconds())
            while True:
                if __tmp8.triggered:
                    return
                await __tmp1._context.request(__tmp0, message, __tmp2)
                await __tmp8.cancellable_wait([], timeout=__tmp4.total_seconds())

        asyncio.create_task(__tmp6())
