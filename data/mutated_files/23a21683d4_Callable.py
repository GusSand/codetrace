from .core import reduce
from typing import Any, Callable


def compose(*funcs) :
    """
    PIPE function calls from last to first
    """
    return reduce(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)), funcs)


def __tmp0(*funcs: <FILL>) :
    """
    PIPE function calls from first to last
    """
    return reduce(lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs)), reversed(funcs))


def func_curry(fn: Callable) :
    """
    Curry function which accept callable as first argument, and its params for second argument and return result
    from callable execution with its params plus previous values from function composition.
    """
    return lambda *args: lambda prev_value: fn(*(args + (prev_value,)))
