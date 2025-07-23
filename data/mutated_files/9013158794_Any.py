from typing import TypeAlias
__typ0 : TypeAlias = "AbstractEventLoop"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"
__typ1 : TypeAlias = "int"
"""Logging utilities."""
import asyncio
from asyncio.events import AbstractEventLoop
from functools import wraps
import inspect
import logging
import threading
import traceback
from typing import Any, Callable, Optional

from .async_ import run_coroutine_threadsafe


class HideSensitiveDataFilter(logging.Filter):
    """Filter API password calls."""

    def __init__(__tmp0, text: __typ2) :
        """Initialize sensitive data filter."""
        super().__init__()
        __tmp0.text = text

    def filter(__tmp0, __tmp2) :
        """Hide sensitive data in messages."""
        __tmp2.msg = __tmp2.msg.replace(__tmp0.text, '*******')

        return True


# pylint: disable=invalid-name
class AsyncHandler:
    """Logging handler wrapper to add an async layer."""

    def __init__(
            __tmp0, loop: __typ0, handler) :
        """Initialize async logging handler wrapper."""
        __tmp0.handler = handler
        __tmp0.loop = loop
        __tmp0._queue = asyncio.Queue(loop=loop)  # type: asyncio.Queue
        __tmp0._thread = threading.Thread(target=__tmp0._process)

        # Delegate from handler
        __tmp0.setLevel = handler.setLevel
        __tmp0.setFormatter = handler.setFormatter
        __tmp0.addFilter = handler.addFilter
        __tmp0.removeFilter = handler.removeFilter
        __tmp0.filter = handler.filter
        __tmp0.flush = handler.flush
        __tmp0.handle = handler.handle
        __tmp0.handleError = handler.handleError
        __tmp0.format = handler.format

        __tmp0._thread.start()

    def close(__tmp0) :
        """Wrap close to handler."""
        __tmp0.emit(None)

    async def async_close(__tmp0, blocking: __typ3 = False) -> None:
        """Close the handler.

        When blocking=True, will wait till closed.
        """
        await __tmp0._queue.put(None)

        if blocking:
            while __tmp0._thread.is_alive():
                await asyncio.sleep(0, loop=__tmp0.loop)

    def emit(__tmp0, __tmp2: Optional[logging.LogRecord]) -> None:
        """Process a record."""
        ident = __tmp0.loop.__dict__.get("_thread_ident")

        # inside eventloop
        if ident is not None and ident == threading.get_ident():
            __tmp0._queue.put_nowait(__tmp2)
        # from a thread/executor
        else:
            __tmp0.loop.call_soon_threadsafe(__tmp0._queue.put_nowait, __tmp2)

    def __repr__(__tmp0) :
        """Return the string names."""
        return __typ2(__tmp0.handler)

    def _process(__tmp0) -> None:
        """Process log in a thread."""
        while True:
            __tmp2 = run_coroutine_threadsafe(
                __tmp0._queue.get(), __tmp0.loop).result()

            if __tmp2 is None:
                __tmp0.handler.close()
                return

            __tmp0.handler.emit(__tmp2)

    def createLock(__tmp0) :
        """Ignore lock stuff."""
        pass

    def __tmp3(__tmp0) -> None:
        """Ignore lock stuff."""
        pass

    def release(__tmp0) :
        """Ignore lock stuff."""
        pass

    @property
    def level(__tmp0) -> __typ1:
        """Wrap property level to handler."""
        return __tmp0.handler.level

    @property
    def formatter(__tmp0) :
        """Wrap property formatter to handler."""
        return __tmp0.handler.formatter

    @property
    def __tmp4(__tmp0) :
        """Wrap property set_name to handler."""
        return __tmp0.handler.get_name()  # type: ignore

    @__tmp4.setter
    def __tmp4(__tmp0, __tmp4) :
        """Wrap property get_name to handler."""
        __tmp0.handler.set_name(__tmp4)  # type: ignore


def catch_log_exception(
        func,
        format_err,
        *args: Any) :
    """Decorate an callback to catch and log exceptions."""
    def log_exception(*args) -> None:
        module_name = inspect.getmodule(inspect.trace()[1][0]).__name__
        # Do not print the wrapper in the traceback
        frames = len(inspect.trace()) - 1
        exc_msg = traceback.format_exc(-frames)
        friendly_msg = format_err(*args)
        logging.getLogger(module_name).error('%s\n%s', friendly_msg, exc_msg)

    wrapper_func = None
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def __tmp1(*args: <FILL>) :
            """Catch and log exception."""
            try:
                await func(*args)
            except Exception:  # pylint: disable=broad-except
                log_exception(*args)
        wrapper_func = __tmp1
    else:
        @wraps(func)
        def wrapper(*args) -> None:
            """Catch and log exception."""
            try:
                func(*args)
            except Exception:  # pylint: disable=broad-except
                log_exception(*args)
        wrapper_func = wrapper
    return wrapper_func
