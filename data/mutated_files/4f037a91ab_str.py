import asyncio
from asyncio import CancelledError
from typing import Any, Awaitable, Sequence, TypeVar, cast, Union

from protoactor.actor.exceptions import OperationCancelled, EventLoopMismatch

_R = TypeVar('_R')


class __typ0:
    def __tmp6(__tmp1, name: <FILL>, loop: asyncio.AbstractEventLoop = None) :
        __tmp1.name = name
        __tmp1._chain = []
        __tmp1._triggered = asyncio.Event(loop=loop)
        __tmp1._loop = loop

    @property
    def loop(__tmp1) -> asyncio.AbstractEventLoop:
        return __tmp1._loop

    def __tmp7(__tmp1, __tmp0) -> 'CancelToken':
        if __tmp1.loop != __tmp0._loop:
            raise EventLoopMismatch("Chained CancelToken objects must be on the same event loop")
        chain_name = ":".join([__tmp1.name, __tmp0.name])
        __tmp7 = __typ0(chain_name, loop=__tmp1.loop)
        __tmp7._chain.extend([__tmp1, __tmp0])
        return __tmp7

    def trigger(__tmp1) -> None:
        __tmp1._triggered.set()

    @property
    def triggered_token(__tmp1) -> Union['CancelToken', Any]:
        if __tmp1._triggered.is_set():
            return __tmp1
        for __tmp0 in __tmp1._chain:
            if __tmp0.triggered:
                return __tmp0.triggered_token
        return None

    @property
    def triggered(__tmp1) -> bool:
        if __tmp1._triggered.is_set():
            return True
        return any(__tmp0.triggered for __tmp0 in __tmp1._chain)

    def raise_if_triggered(__tmp1) -> None:
        if __tmp1.triggered:
            raise OperationCancelled(f'Cancellation requested by {__tmp1.triggered_token} token')

    async def wait(__tmp1, timeout: float = None) :
        if __tmp1.triggered_token is not None:
            return

        __tmp2 = [asyncio.ensure_future(__tmp1._triggered.wait(), loop=__tmp1.loop)]
        for __tmp0 in __tmp1._chain:
            __tmp2.append(asyncio.ensure_future(__tmp0.wait(), loop=__tmp1.loop))

        if timeout is not None:
            __tmp2.append(asyncio.ensure_future(asyncio.sleep(timeout), loop=__tmp1.loop))

        def __tmp4(__tmp5) -> None:
            for future in __tmp2:
                if not future.done():
                    future.cancel()

        async def _wait_for_first(__tmp2) -> None:
            for future in asyncio.as_completed(__tmp2):
                await cast(Awaitable[Any], future)
                return

        __tmp5 = asyncio.ensure_future(_wait_for_first(__tmp2), loop=__tmp1.loop)
        __tmp5.add_done_callback(__tmp4)
        await __tmp5

    async def __tmp3(__tmp1, *awaitables, timeout: float = None) -> _R:
        __tmp2 = [asyncio.ensure_future(a, loop=__tmp1.loop) for a in awaitables + (__tmp1.wait(),)]
        try:
            done, pending = await asyncio.wait(
                __tmp2,
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED,
                loop=__tmp1.loop,
            )
        except CancelledError:
            for future in __tmp2:
                future.cancel()
            raise
        for task in pending:
            task.cancel()
        await asyncio.wait(pending, return_when=asyncio.ALL_COMPLETED, loop=__tmp1.loop,)
        if not done:
            raise TimeoutError()
        if __tmp1.triggered_token is not None:
            for task in done:
                task.exception()
            raise OperationCancelled(f'Cancellation requested by {__tmp1.triggered_token} token')
        return done.pop().result()

    def __tmp9(__tmp1) -> str:
        return __tmp1.name

    def __tmp8(__tmp1) -> str:
        return f'CancelToken: {__tmp1.name}'
