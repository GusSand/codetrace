
import sys
import functools

from typing import Any, Callable, IO, Mapping, Sequence, TypeVar

def __tmp5(__tmp6) :
    container_type = type(__tmp6).__name__
    if not __tmp6:
        if container_type == 'dict':
            return '{}'
        else:
            return container_type + '([])'
    key = next(iter(__tmp6))
    key_type = __tmp0(key)
    value_type = __tmp0(__tmp6[key])
    if container_type == 'dict':
        if len(__tmp6) == 1:
            return '{%s: %s}' % (key_type, value_type)
        else:
            return '{%s: %s, ...}' % (key_type, value_type)
    else:
        if len(__tmp6) == 1:
            return '%s([(%s, %s)])' % (container_type, key_type, value_type)
        else:
            return '%s([(%s, %s), ...])' % (container_type, key_type, value_type)

def get_sequence_type_str(__tmp6) :
    container_type = type(__tmp6).__name__
    if not __tmp6:
        if container_type == 'list':
            return '[]'
        else:
            return container_type + '([])'
    elem_type = __tmp0(__tmp6[0])
    if container_type == 'list':
        if len(__tmp6) == 1:
            return '[' + elem_type + ']'
        else:
            return '[' + elem_type + ', ...]'
    else:
        if len(__tmp6) == 1:
            return '%s([%s])' % (container_type, elem_type)
        else:
            return '%s([%s, ...])' % (container_type, elem_type)

expansion_blacklist = [str, bytes]

def __tmp0(__tmp6: <FILL>) :
    if __tmp6 is None:
        return 'None'
    elif isinstance(__tmp6, tuple):
        types = []
        for v in __tmp6:
            types.append(__tmp0(v))
        if len(__tmp6) == 1:
            return '(' + types[0] + ',)'
        else:
            return '(' + ', '.join(types) + ')'
    elif isinstance(__tmp6, Mapping):
        return __tmp5(__tmp6)
    elif isinstance(__tmp6, Sequence) and not any(isinstance(__tmp6, t) for t in expansion_blacklist):
        return get_sequence_type_str(__tmp6)
    else:
        return type(__tmp6).__name__

FuncT = TypeVar('FuncT', bound=Callable[..., Any])

def __tmp4(file_obj) :
    def __tmp2(func) :
        @functools.wraps(func)
        def __tmp3(*args, **kwargs) :
            arg_types = [__tmp0(arg) for arg in args]
            kwarg_types = [key + "=" + __tmp0(value) for key, value in kwargs.items()]
            ret_val = func(*args, **kwargs)
            output = "%s(%s) -> %s" % (func.__name__,
                                       ", ".join(arg_types + kwarg_types),
                                       __tmp0(ret_val))
            print(output, file=file_obj)
            return ret_val
        return __tmp3  # type: ignore # https://github.com/python/mypy/issues/1927
    return __tmp2

def __tmp1(func) :
    return __tmp4(sys.stdout)(func)
