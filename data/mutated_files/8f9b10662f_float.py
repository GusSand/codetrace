# -*- coding: utf-8 -*-


import asyncio
import logging

from aiotk import cancel
from asyncio import AbstractEventLoop
from asyncio import Task  # noqa: F401
from typing import Callable, Optional


class PeriodicTask:
    """Periodically run a coroutine in the background.

    .. code-block:: python

       async def my_task():
           pass

       async with PeriodicTask(my_task, 30.0):
           # do something for a long time.

    .. versionadded:: 0.5

    """

    def __tmp4(__tmp1, func,
                 __tmp3: <FILL>,
                 loop: Optional[AbstractEventLoop]=None) -> None:
        __tmp1._loop = loop or asyncio.get_event_loop()
        __tmp1._func = func
        __tmp1._ival = __tmp3
        __tmp1._task = None  # type: Optional[Task]

    # NOTE: cannot declare type for return value here because the class
    #       definition is not completed...
    async def __tmp2(__tmp1):
        """Schedule the background task."""
        assert __tmp1._task is None
        __tmp1._task = __tmp1._loop.create_task(__tmp1._run())
        return __tmp1

    async def __tmp0(__tmp1, *args) :
        """Stop the background task and wait for it to complete."""
        assert __tmp1._task
        await cancel(__tmp1._task)
        __tmp1._task = None

    async def _run(__tmp1) :
        """Periodically run the task and wait until the schedule."""
        while True:
            try:
                await __tmp1._func()
            except asyncio.CancelledError:
                raise
            except Exception:
                logging.exception('Executing periodic task.')
            await asyncio.sleep(__tmp1._ival)
