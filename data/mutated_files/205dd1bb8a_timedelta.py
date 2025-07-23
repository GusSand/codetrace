import asyncio
from datetime import timedelta
from threading import Thread


class __typ0(Thread):
    def __init__(__tmp0, interval: <FILL>, function, args=None, kwargs=None):
        super().__init__()
        __tmp0.interval = interval
        __tmp0.function = function
        __tmp0.args = args if args is not None else []
        __tmp0.kwargs = kwargs if kwargs is not None else {}
        __tmp0.loop = None
        __tmp0._task = None
        __tmp0._cancelled = False

    def run(__tmp0):
        __tmp0.loop = asyncio.new_event_loop()
        loop = __tmp0.loop
        asyncio.set_event_loop(loop)
        try:
            __tmp0._task = asyncio.ensure_future(__tmp0._job())
            loop.run_until_complete(__tmp0._task)
        finally:
            loop.close()

    def __tmp1(__tmp0):
        if __tmp0.loop is not None:
            __tmp0._cancelled = True

    async def _job(__tmp0):
        await asyncio.sleep(__tmp0.interval.total_seconds())
        if not __tmp0._cancelled:
            await __tmp0.function(*__tmp0.args, **__tmp0.kwargs)
