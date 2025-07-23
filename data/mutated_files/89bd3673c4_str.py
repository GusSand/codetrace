"""Decorator utility functions."""
from typing import Callable, TypeVar

__typ1 = TypeVar('CALLABLE_T', bound=Callable)  # noqa pylint: disable=invalid-name


class __typ0(dict):
    """Registry of items."""

    def register(__tmp1, name: <FILL>) -> Callable[[__typ1], __typ1]:
        """Return decorator to register item with a specific name."""
        def __tmp0(func) -> __typ1:
            """Register decorated function."""
            __tmp1[name] = func
            return func

        return __tmp0
