from typing import TypeAlias
__typ1 : TypeAlias = "any"
__typ2 : TypeAlias = "timedelta"
import asyncio
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext, RootContext
from protoactor.actor.cancel_token import CancelToken


class AbstractSimpleScheduler(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp4(__tmp2, __tmp11: __typ2, __tmp1: PID, __tmp0: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp2, __tmp11: __typ2, __tmp5: __typ2, __tmp1: PID, __tmp0: __typ1,
                                       __tmp9) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp2, __tmp11: __typ2, __tmp3: PID, __tmp1: PID,
                                    __tmp0: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp10(__tmp2, __tmp11: __typ2, __tmp5: __typ2, __tmp3: PID, __tmp1: PID,
                                          __tmp0: __typ1,
                                          __tmp9: CancelToken) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ0(AbstractSimpleScheduler):
    def __init__(__tmp2, context: AbstractSenderContext = RootContext()):
        __tmp2._context = context

    async def __tmp4(__tmp2, __tmp11: __typ2, __tmp1: PID, __tmp0: __typ1) -> None:
        async def __tmp8():
            await asyncio.sleep(__tmp11.total_seconds())
            await __tmp2._context.send(__tmp1, __tmp0)

        asyncio.create_task(__tmp8())

    async def __tmp7(__tmp2, __tmp11: __typ2, __tmp5: __typ2, __tmp1: PID, __tmp0: __typ1,
                                       __tmp9: CancelToken) :
        async def __tmp8():
            await __tmp9.wait(__tmp11.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.send(__tmp1, __tmp0)
                await __tmp9.wait(__tmp5.total_seconds())

        asyncio.create_task(__tmp8())

    async def __tmp6(__tmp2, __tmp11: __typ2, __tmp3: PID, __tmp1: PID,
                                    __tmp0: __typ1) -> None:
        async def __tmp8():
            await asyncio.sleep(__tmp11.total_seconds())
            await __tmp2._context.request(__tmp1, __tmp0, __tmp3)

        asyncio.create_task(__tmp8())

    async def __tmp10(__tmp2, __tmp11, __tmp5: __typ2, __tmp3: PID, __tmp1: <FILL>,
                                          __tmp0: __typ1, __tmp9: CancelToken) -> None:
        async def __tmp8():
            await __tmp9.cancellable_wait([], timeout=__tmp11.total_seconds())
            while True:
                if __tmp9.triggered:
                    return
                await __tmp2._context.request(__tmp1, __tmp0, __tmp3)
                await __tmp9.cancellable_wait([], timeout=__tmp5.total_seconds())

        asyncio.create_task(__tmp8())
