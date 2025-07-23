from typing import TypeAlias
__typ0 : TypeAlias = "CancelToken"
__typ1 : TypeAlias = "PID"
__typ2 : TypeAlias = "any"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp4(__tmp2, __tmp7: timedelta, __tmp1: __typ1, __tmp0: __typ2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp2, __tmp7, __tmp3: timedelta, __tmp1, __tmp0: __typ2,
                                       __tmp6: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_once(__tmp2, __tmp7: timedelta, sender: __typ1, __tmp1: __typ1,
                                    __tmp0: __typ2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def schedule_request_repeatedly(__tmp2, __tmp7: timedelta, __tmp3: <FILL>, sender: __typ1, __tmp1: __typ1,
                                          __tmp0: __typ2,
                                          __tmp6: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")


class SimpleScheduler(AbstractSimpleScheduler):
    def __init__(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp4(__tmp2, __tmp7, __tmp1: __typ1, __tmp0: __typ2) -> None:
        async def schedule():
            await asyncio.sleep(__tmp7.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(schedule())

    async def __tmp5(__tmp2, __tmp7: timedelta, __tmp3: timedelta, __tmp1: __typ1, __tmp0: __typ2,
                                       __tmp6: __typ0) -> None:
        async def schedule():
            await __tmp6.wait(__tmp7.total_seconds())
            while True:
                if __tmp6.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp6.wait(__tmp3.total_seconds())

        asyncio.create_task(schedule())

    async def schedule_request_once(__tmp2, __tmp7: timedelta, sender: __typ1, __tmp1: __typ1,
                                    __tmp0) -> None:
        async def schedule():
            await asyncio.sleep(__tmp7.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, sender)

        asyncio.create_task(schedule())

    async def schedule_request_repeatedly(__tmp2, __tmp7: timedelta, __tmp3: timedelta, sender: __typ1, __tmp1: __typ1,
                                          __tmp0: __typ2, __tmp6: __typ0) -> None:
        async def schedule():
            await __tmp6.cancellable_wait([], timeout=__tmp7.total_seconds())
            while True:
                if __tmp6.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, sender)
                await __tmp6.cancellable_wait([], timeout=__tmp3.total_seconds())

        asyncio.create_task(schedule())
