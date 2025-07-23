from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "timedelta"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp2, __tmp10, __tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp2, __tmp10, __tmp3, __tmp1, __tmp0,
                                       __tmp8) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_once(__tmp2, __tmp10, __tmp4, __tmp1,
                                    __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp9(__tmp2, __tmp10, __tmp3, __tmp4: <FILL>, __tmp1,
                                          __tmp0,
                                          __tmp8) :
        raise NotImplementedError("Should Implement this method")


class SimpleScheduler(AbstractSimpleScheduler):
    def __init__(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp5(__tmp2, __tmp10, __tmp1, __tmp0) :
        async def __tmp7():
            await asyncio.sleep(__tmp10.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp7())

    async def __tmp6(__tmp2, __tmp10, __tmp3, __tmp1, __tmp0,
                                       __tmp8) :
        async def __tmp7():
            await __tmp8.wait(__tmp10.total_seconds())
            while True:
                if __tmp8.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp8.wait(__tmp3.total_seconds())

        asyncio.create_task(__tmp7())

    async def schedule_request_once(__tmp2, __tmp10, __tmp4, __tmp1,
                                    __tmp0) :
        async def __tmp7():
            await asyncio.sleep(__tmp10.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp4)

        asyncio.create_task(__tmp7())

    async def __tmp9(__tmp2, __tmp10: __typ1, __tmp3, __tmp4, __tmp1,
                                          __tmp0, __tmp8) :
        async def __tmp7():
            await __tmp8.cancellable_wait([], timeout=__tmp10.total_seconds())
            while True:
                if __tmp8.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp4)
                await __tmp8.cancellable_wait([], timeout=__tmp3.total_seconds())

        asyncio.create_task(__tmp7())
