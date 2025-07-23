from typing import TypeAlias
__typ0 : TypeAlias = "str"

import sys
import functools

from typing import Any, Callable, IO, Mapping, Sequence, TypeVar

def __tmp1(__tmp2: Mapping[Any, Any]) -> __typ0:
    container_type = type(__tmp2).__name__
    if not __tmp2:
        if container_type == 'dict':
            return '{}'
        else:
            return container_type + '([])'
    key = next(iter(__tmp2))
    key_type = get_type_str(key)
    value_type = get_type_str(__tmp2[key])
    if container_type == 'dict':
        if len(__tmp2) == 1:
            return '{%s: %s}' % (key_type, value_type)
        else:
            return '{%s: %s, ...}' % (key_type, value_type)
    else:
        if len(__tmp2) == 1:
            return '%s([(%s, %s)])' % (container_type, key_type, value_type)
        else:
            return '%s([(%s, %s), ...])' % (container_type, key_type, value_type)

def get_sequence_type_str(__tmp2: Sequence[Any]) -> __typ0:
    container_type = type(__tmp2).__name__
    if not __tmp2:
        if container_type == 'list':
            return '[]'
        else:
            return container_type + '([])'
    elem_type = get_type_str(__tmp2[0])
    if container_type == 'list':
        if len(__tmp2) == 1:
            return '[' + elem_type + ']'
        else:
            return '[' + elem_type + ', ...]'
    else:
        if len(__tmp2) == 1:
            return '%s([%s])' % (container_type, elem_type)
        else:
            return '%s([%s, ...])' % (container_type, elem_type)

expansion_blacklist = [__typ0, bytes]

def get_type_str(__tmp2) -> __typ0:
    if __tmp2 is None:
        return 'None'
    elif isinstance(__tmp2, tuple):
        types = []
        for v in __tmp2:
            types.append(get_type_str(v))
        if len(__tmp2) == 1:
            return '(' + types[0] + ',)'
        else:
            return '(' + ', '.join(types) + ')'
    elif isinstance(__tmp2, Mapping):
        return __tmp1(__tmp2)
    elif isinstance(__tmp2, Sequence) and not any(isinstance(__tmp2, t) for t in expansion_blacklist):
        return get_sequence_type_str(__tmp2)
    else:
        return type(__tmp2).__name__

__typ1 = TypeVar('FuncT', bound=Callable[..., Any])

def print_types_to(file_obj: IO[__typ0]) :
    def __tmp0(func) -> __typ1:
        @functools.wraps(func)
        def wrapper(*args: <FILL>, **kwargs: Any) -> Any:
            arg_types = [get_type_str(arg) for arg in args]
            kwarg_types = [key + "=" + get_type_str(value) for key, value in kwargs.items()]
            ret_val = func(*args, **kwargs)
            output = "%s(%s) -> %s" % (func.__name__,
                                       ", ".join(arg_types + kwarg_types),
                                       get_type_str(ret_val))
            print(output, file=file_obj)
            return ret_val
        return wrapper  # type: ignore # https://github.com/python/mypy/issues/1927
    return __tmp0

def print_types(func: __typ1) -> __typ1:
    return print_types_to(sys.stdout)(func)
