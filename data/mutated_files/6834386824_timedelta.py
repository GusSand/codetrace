from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "PID"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def schedule_tell_once(__tmp2, __tmp9, __tmp1: __typ1, __tmp0: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_tell_repeatedly(__tmp2, __tmp9: timedelta, __tmp4, __tmp1: __typ1, __tmp0: __typ0,
                                       __tmp7: CancelToken) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp2, __tmp9, __tmp3: __typ1, __tmp1: __typ1,
                                    __tmp0: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp8(__tmp2, __tmp9: <FILL>, __tmp4: timedelta, __tmp3: __typ1, __tmp1,
                                          __tmp0: __typ0,
                                          __tmp7: CancelToken) -> None:
        raise NotImplementedError("Should Implement this method")


class SimpleScheduler(AbstractSimpleScheduler):
    def __init__(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def schedule_tell_once(__tmp2, __tmp9, __tmp1: __typ1, __tmp0: __typ0) :
        async def __tmp6():
            await asyncio.sleep(__tmp9.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp6())

    async def schedule_tell_repeatedly(__tmp2, __tmp9: timedelta, __tmp4: timedelta, __tmp1, __tmp0,
                                       __tmp7) -> None:
        async def __tmp6():
            await __tmp7.wait(__tmp9.total_seconds())
            while True:
                if __tmp7.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp7.wait(__tmp4.total_seconds())

        asyncio.create_task(__tmp6())

    async def __tmp5(__tmp2, __tmp9, __tmp3: __typ1, __tmp1: __typ1,
                                    __tmp0: __typ0) -> None:
        async def __tmp6():
            await asyncio.sleep(__tmp9.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp3)

        asyncio.create_task(__tmp6())

    async def __tmp8(__tmp2, __tmp9: timedelta, __tmp4, __tmp3: __typ1, __tmp1: __typ1,
                                          __tmp0: __typ0, __tmp7: CancelToken) -> None:
        async def __tmp6():
            await __tmp7.cancellable_wait([], timeout=__tmp9.total_seconds())
            while True:
                if __tmp7.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp3)
                await __tmp7.cancellable_wait([], timeout=__tmp4.total_seconds())

        asyncio.create_task(__tmp6())
