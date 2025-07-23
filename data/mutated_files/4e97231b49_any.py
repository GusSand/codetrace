from typing import TypeAlias
__typ1 : TypeAlias = "CancelToken"
__typ2 : TypeAlias = "timedelta"
__typ0 : TypeAlias = "PID"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class __typ4(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp2, __tmp11: __typ2, __tmp1: __typ0, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp2, __tmp11: __typ2, __tmp3: __typ2, __tmp1: __typ0, __tmp0: <FILL>,
                                       __tmp9: __typ1) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp2, __tmp11, __tmp4: __typ0, __tmp1,
                                    __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp10(__tmp2, __tmp11: __typ2, __tmp3: __typ2, __tmp4: __typ0, __tmp1: __typ0,
                                          __tmp0: any,
                                          __tmp9: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ3(__typ4):
    def __init__(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp5(__tmp2, __tmp11: __typ2, __tmp1, __tmp0: any) :
        async def __tmp8():
            await asyncio.sleep(__tmp11.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp8())

    async def __tmp7(__tmp2, __tmp11: __typ2, __tmp3: __typ2, __tmp1: __typ0, __tmp0: any,
                                       __tmp9: __typ1) -> None:
        async def __tmp8():
            await __tmp9.wait(__tmp11.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp9.wait(__tmp3.total_seconds())

        asyncio.create_task(__tmp8())

    async def __tmp6(__tmp2, __tmp11: __typ2, __tmp4: __typ0, __tmp1: __typ0,
                                    __tmp0: any) -> None:
        async def __tmp8():
            await asyncio.sleep(__tmp11.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp4)

        asyncio.create_task(__tmp8())

    async def __tmp10(__tmp2, __tmp11: __typ2, __tmp3: __typ2, __tmp4, __tmp1: __typ0,
                                          __tmp0, __tmp9: __typ1) :
        async def __tmp8():
            await __tmp9.cancellable_wait([], timeout=__tmp11.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp4)
                await __tmp9.cancellable_wait([], timeout=__tmp3.total_seconds())

        asyncio.create_task(__tmp8())
