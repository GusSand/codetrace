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
    async def __tmp5(__tmp2, __tmp10, __tmp1: PID, __tmp0: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp2, __tmp10: __typ2, __tmp3, __tmp1: <FILL>, __tmp0,
                                       __tmp9: __typ1) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_once(__tmp2, __tmp10: __typ2, __tmp4: PID, __tmp1: PID,
                                    __tmp0: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_repeatedly(__tmp2, __tmp10: __typ2, __tmp3, __tmp4: PID, __tmp1,
                                          __tmp0: __typ0,
                                          __tmp9: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ3(__typ4):
    def __tmp8(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp5(__tmp2, __tmp10, __tmp1: PID, __tmp0: __typ0) -> None:
        async def __tmp7():
            await asyncio.sleep(__tmp10.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp7())

    async def __tmp6(__tmp2, __tmp10: __typ2, __tmp3, __tmp1: PID, __tmp0: __typ0,
                                       __tmp9) -> None:
        async def __tmp7():
            await __tmp9.wait(__tmp10.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp9.wait(__tmp3.total_seconds())

        asyncio.create_task(__tmp7())

    async def schedule_request_once(__tmp2, __tmp10: __typ2, __tmp4, __tmp1,
                                    __tmp0) :
        async def __tmp7():
            await asyncio.sleep(__tmp10.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp4)

        asyncio.create_task(__tmp7())

    async def schedule_request_repeatedly(__tmp2, __tmp10, __tmp3: __typ2, __tmp4: PID, __tmp1,
                                          __tmp0, __tmp9: __typ1) -> None:
        async def __tmp7():
            await __tmp9.cancellable_wait([], timeout=__tmp10.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp4)
                await __tmp9.cancellable_wait([], timeout=__tmp3.total_seconds())

        asyncio.create_task(__tmp7())
