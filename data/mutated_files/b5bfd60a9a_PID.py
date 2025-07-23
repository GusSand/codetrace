from typing import TypeAlias
__typ0 : TypeAlias = "CancelToken"
__typ2 : TypeAlias = "any"
__typ1 : TypeAlias = "timedelta"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp4(__tmp2, __tmp11: __typ1, __tmp1: PID, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp2, __tmp11, __tmp3: __typ1, __tmp1: PID, __tmp0,
                                       __tmp9) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp2, __tmp11, __tmp5, __tmp1,
                                    __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp10(__tmp2, __tmp11, __tmp3, __tmp5, __tmp1: PID,
                                          __tmp0,
                                          __tmp9) :
        raise NotImplementedError("Should Implement this method")


class SimpleScheduler(AbstractSimpleScheduler):
    def __tmp8(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp4(__tmp2, __tmp11: __typ1, __tmp1: PID, __tmp0: __typ2) -> None:
        async def schedule():
            await asyncio.sleep(__tmp11.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(schedule())

    async def __tmp7(__tmp2, __tmp11, __tmp3, __tmp1: <FILL>, __tmp0,
                                       __tmp9) :
        async def schedule():
            await __tmp9.wait(__tmp11.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp9.wait(__tmp3.total_seconds())

        asyncio.create_task(schedule())

    async def __tmp6(__tmp2, __tmp11, __tmp5: PID, __tmp1,
                                    __tmp0: __typ2) :
        async def schedule():
            await asyncio.sleep(__tmp11.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp5)

        asyncio.create_task(schedule())

    async def __tmp10(__tmp2, __tmp11, __tmp3: __typ1, __tmp5, __tmp1,
                                          __tmp0: __typ2, __tmp9) -> None:
        async def schedule():
            await __tmp9.cancellable_wait([], timeout=__tmp11.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp5)
                await __tmp9.cancellable_wait([], timeout=__tmp3.total_seconds())

        asyncio.create_task(schedule())
