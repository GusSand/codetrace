from typing import TypeAlias
__typ0 : TypeAlias = "str"

import sys
import functools

from typing import Any, Callable, IO, Mapping, Sequence, TypeVar

def __tmp6(__tmp8) -> __typ0:
    container_type = type(__tmp8).__name__
    if not __tmp8:
        if container_type == 'dict':
            return '{}'
        else:
            return container_type + '([])'
    key = next(iter(__tmp8))
    key_type = __tmp1(key)
    value_type = __tmp1(__tmp8[key])
    if container_type == 'dict':
        if len(__tmp8) == 1:
            return '{%s: %s}' % (key_type, value_type)
        else:
            return '{%s: %s, ...}' % (key_type, value_type)
    else:
        if len(__tmp8) == 1:
            return '%s([(%s, %s)])' % (container_type, key_type, value_type)
        else:
            return '%s([(%s, %s), ...])' % (container_type, key_type, value_type)

def __tmp0(__tmp8) -> __typ0:
    container_type = type(__tmp8).__name__
    if not __tmp8:
        if container_type == 'list':
            return '[]'
        else:
            return container_type + '([])'
    elem_type = __tmp1(__tmp8[0])
    if container_type == 'list':
        if len(__tmp8) == 1:
            return '[' + elem_type + ']'
        else:
            return '[' + elem_type + ', ...]'
    else:
        if len(__tmp8) == 1:
            return '%s([%s])' % (container_type, elem_type)
        else:
            return '%s([%s, ...])' % (container_type, elem_type)

expansion_blacklist = [__typ0, bytes]

def __tmp1(__tmp8: Any) -> __typ0:
    if __tmp8 is None:
        return 'None'
    elif isinstance(__tmp8, tuple):
        types = []
        for v in __tmp8:
            types.append(__tmp1(v))
        if len(__tmp8) == 1:
            return '(' + types[0] + ',)'
        else:
            return '(' + ', '.join(types) + ')'
    elif isinstance(__tmp8, Mapping):
        return __tmp6(__tmp8)
    elif isinstance(__tmp8, Sequence) and not any(isinstance(__tmp8, t) for t in expansion_blacklist):
        return __tmp0(__tmp8)
    else:
        return type(__tmp8).__name__

__typ1 = TypeVar('FuncT', bound=Callable[..., Any])

def __tmp5(__tmp7) :
    def __tmp2(func: __typ1) -> __typ1:
        @functools.wraps(func)
        def __tmp4(*args: Any, **kwargs: <FILL>) :
            arg_types = [__tmp1(arg) for arg in args]
            kwarg_types = [key + "=" + __tmp1(value) for key, value in kwargs.items()]
            ret_val = func(*args, **kwargs)
            output = "%s(%s) -> %s" % (func.__name__,
                                       ", ".join(arg_types + kwarg_types),
                                       __tmp1(ret_val))
            print(output, file=__tmp7)
            return ret_val
        return __tmp4  # type: ignore # https://github.com/python/mypy/issues/1927
    return __tmp2

def __tmp3(func) :
    return __tmp5(sys.stdout)(func)
