from typing import TypeAlias
__typ0 : TypeAlias = "float"
# -*- coding: utf-8 -*-


import asyncio
import logging

from aiotk import cancel
from asyncio import AbstractEventLoop
from asyncio import Task  # noqa: F401
from typing import Callable, Optional


class __typ1:
    """Periodically run a coroutine in the background.

    .. code-block:: python

       async def my_task():
           pass

       async with PeriodicTask(my_task, 30.0):
           # do something for a long time.

    .. versionadded:: 0.5

    """

    def __init__(__tmp0, func: <FILL>,
                 interval: __typ0,
                 loop: Optional[AbstractEventLoop]=None) -> None:
        __tmp0._loop = loop or asyncio.get_event_loop()
        __tmp0._func = func
        __tmp0._ival = interval
        __tmp0._task = None  # type: Optional[Task]

    # NOTE: cannot declare type for return value here because the class
    #       definition is not completed...
    async def __tmp1(__tmp0):
        """Schedule the background task."""
        assert __tmp0._task is None
        __tmp0._task = __tmp0._loop.create_task(__tmp0._run())
        return __tmp0

    async def __aexit__(__tmp0, *args) -> None:
        """Stop the background task and wait for it to complete."""
        assert __tmp0._task
        await cancel(__tmp0._task)
        __tmp0._task = None

    async def _run(__tmp0) -> None:
        """Periodically run the task and wait until the schedule."""
        while True:
            try:
                await __tmp0._func()
            except asyncio.CancelledError:
                raise
            except Exception:
                logging.exception('Executing periodic task.')
            await asyncio.sleep(__tmp0._ival)
