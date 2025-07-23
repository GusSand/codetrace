from typing import TypeAlias
__typ0 : TypeAlias = "int"
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

    def __init__(__tmp1, text: <FILL>) -> None:
        """Initialize sensitive data filter."""
        super().__init__()
        __tmp1.text = text

    def filter(__tmp1, __tmp2: logging.LogRecord) -> bool:
        """Hide sensitive data in messages."""
        __tmp2.msg = __tmp2.msg.replace(__tmp1.text, '*******')

        return True


# pylint: disable=invalid-name
class AsyncHandler:
    """Logging handler wrapper to add an async layer."""

    def __init__(
            __tmp1, loop: AbstractEventLoop, handler: logging.Handler) -> None:
        """Initialize async logging handler wrapper."""
        __tmp1.handler = handler
        __tmp1.loop = loop
        __tmp1._queue = asyncio.Queue(loop=loop)  # type: asyncio.Queue
        __tmp1._thread = threading.Thread(target=__tmp1._process)

        # Delegate from handler
        __tmp1.setLevel = handler.setLevel
        __tmp1.setFormatter = handler.setFormatter
        __tmp1.addFilter = handler.addFilter
        __tmp1.removeFilter = handler.removeFilter
        __tmp1.filter = handler.filter
        __tmp1.flush = handler.flush
        __tmp1.handle = handler.handle
        __tmp1.handleError = handler.handleError
        __tmp1.format = handler.format

        __tmp1._thread.start()

    def close(__tmp1) -> None:
        """Wrap close to handler."""
        __tmp1.emit(None)

    async def async_close(__tmp1, blocking: bool = False) -> None:
        """Close the handler.

        When blocking=True, will wait till closed.
        """
        await __tmp1._queue.put(None)

        if blocking:
            while __tmp1._thread.is_alive():
                await asyncio.sleep(0, loop=__tmp1.loop)

    def emit(__tmp1, __tmp2: Optional[logging.LogRecord]) -> None:
        """Process a record."""
        ident = __tmp1.loop.__dict__.get("_thread_ident")

        # inside eventloop
        if ident is not None and ident == threading.get_ident():
            __tmp1._queue.put_nowait(__tmp2)
        # from a thread/executor
        else:
            __tmp1.loop.call_soon_threadsafe(__tmp1._queue.put_nowait, __tmp2)

    def __repr__(__tmp1) -> str:
        """Return the string names."""
        return str(__tmp1.handler)

    def _process(__tmp1) -> None:
        """Process log in a thread."""
        while True:
            __tmp2 = run_coroutine_threadsafe(
                __tmp1._queue.get(), __tmp1.loop).result()

            if __tmp2 is None:
                __tmp1.handler.close()
                return

            __tmp1.handler.emit(__tmp2)

    def createLock(__tmp1) -> None:
        """Ignore lock stuff."""
        pass

    def acquire(__tmp1) -> None:
        """Ignore lock stuff."""
        pass

    def release(__tmp1) -> None:
        """Ignore lock stuff."""
        pass

    @property
    def level(__tmp1) -> __typ0:
        """Wrap property level to handler."""
        return __tmp1.handler.level

    @property
    def formatter(__tmp1) -> Optional[logging.Formatter]:
        """Wrap property formatter to handler."""
        return __tmp1.handler.formatter

    @property
    def name(__tmp1) -> str:
        """Wrap property set_name to handler."""
        return __tmp1.handler.get_name()  # type: ignore

    @name.setter
    def name(__tmp1, name: str) -> None:
        """Wrap property get_name to handler."""
        __tmp1.handler.set_name(name)  # type: ignore


def catch_log_exception(
        func: Callable[..., Any],
        format_err,
        *args: Any) -> Callable[[], None]:
    """Decorate an callback to catch and log exceptions."""
    def log_exception(*args: Any) -> None:
        module_name = inspect.getmodule(inspect.trace()[1][0]).__name__
        # Do not print the wrapper in the traceback
        frames = len(inspect.trace()) - 1
        exc_msg = traceback.format_exc(-frames)
        friendly_msg = format_err(*args)
        logging.getLogger(module_name).error('%s\n%s', friendly_msg, exc_msg)

    wrapper_func = None
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args: Any) :
            """Catch and log exception."""
            try:
                await func(*args)
            except Exception:  # pylint: disable=broad-except
                log_exception(*args)
        wrapper_func = async_wrapper
    else:
        @wraps(func)
        def __tmp0(*args: Any) :
            """Catch and log exception."""
            try:
                func(*args)
            except Exception:  # pylint: disable=broad-except
                log_exception(*args)
        wrapper_func = __tmp0
    return wrapper_func
