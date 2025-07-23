from typing import TypeAlias
__typ0 : TypeAlias = "timedelta"
__typ1 : TypeAlias = "PID"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp4(__tmp2, __tmp12: __typ0, __tmp1: __typ1, __tmp0: any) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp2, __tmp12: __typ0, __tmp3: __typ0, __tmp1: __typ1, __tmp0: any,
                                       __tmp10: CancelToken) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp2, __tmp12: __typ0, __tmp6: __typ1, __tmp1,
                                    __tmp0: any) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp11(__tmp2, __tmp12: __typ0, __tmp3: __typ0, __tmp6: __typ1, __tmp1: __typ1,
                                          __tmp0: any,
                                          __tmp10: CancelToken) -> None:
        raise NotImplementedError("Should Implement this method")


class SimpleScheduler(AbstractSimpleScheduler):
    def __tmp8(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp4(__tmp2, __tmp12: __typ0, __tmp1: __typ1, __tmp0: any) -> None:
        async def __tmp9():
            await asyncio.sleep(__tmp12.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp9())

    async def __tmp7(__tmp2, __tmp12: __typ0, __tmp3: __typ0, __tmp1: __typ1, __tmp0: any,
                                       __tmp10: CancelToken) -> None:
        async def __tmp9():
            await __tmp10.wait(__tmp12.total_seconds())
            while True:
                if __tmp10.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp10.wait(__tmp3.total_seconds())

        asyncio.create_task(__tmp9())

    async def __tmp5(__tmp2, __tmp12: __typ0, __tmp6, __tmp1: __typ1,
                                    __tmp0: <FILL>) -> None:
        async def __tmp9():
            await asyncio.sleep(__tmp12.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp6)

        asyncio.create_task(__tmp9())

    async def __tmp11(__tmp2, __tmp12: __typ0, __tmp3: __typ0, __tmp6: __typ1, __tmp1: __typ1,
                                          __tmp0: any, __tmp10: CancelToken) -> None:
        async def __tmp9():
            await __tmp10.cancellable_wait([], timeout=__tmp12.total_seconds())
            while True:
                if __tmp10.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp6)
                await __tmp10.cancellable_wait([], timeout=__tmp3.total_seconds())

        asyncio.create_task(__tmp9())
