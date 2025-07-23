from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""Find all objects reachable from a root object."""

from collections import deque
from collections.abc import Iterable
from typing import List, Dict, Iterator, Optional, Tuple, Mapping
import weakref
import types


method_descriptor_type = type(object.__dir__)
method_wrapper_type = type(object().__ne__)
wrapper_descriptor_type = type(object.__ne__)

FUNCTION_TYPES = (types.BuiltinFunctionType,
                  types.FunctionType,
                  types.MethodType,
                  method_descriptor_type,
                  wrapper_descriptor_type,
                  method_wrapper_type)

ATTR_BLACKLIST = {
    '__doc__',
    '__name__',
    '__class__',
    '__dict__',
}

# Instances of these types can't have references to other objects
ATOMIC_TYPE_BLACKLIST = {
    __typ0,
    int,
    float,
    str,
    type(None),
    object,
}

# Don't look at most attributes of these types
COLLECTION_TYPE_BLACKLIST = {
    list,
    set,
    dict,
    tuple,
}

# Don't return these objects
TYPE_BLACKLIST = {
    weakref.ReferenceType,
}


def isproperty(o, attr) :
    return isinstance(getattr(type(o), attr, None), property)


def __tmp0(o) :
    if type(o) not in COLLECTION_TYPE_BLACKLIST:
        for attr in dir(o):
            if attr not in ATTR_BLACKLIST and hasattr(o, attr) and not isproperty(o, attr):
                e = getattr(o, attr)
                if not type(e) in ATOMIC_TYPE_BLACKLIST:
                    yield attr, e
    if isinstance(o, Mapping):
        for k, v in o.items():
            yield k, v
    elif isinstance(o, Iterable) and not isinstance(o, str):
        for i, e in enumerate(o):
            yield i, e


def __tmp5(o) :
    for s, e in __tmp0(o):
        if (isinstance(e, FUNCTION_TYPES)):
            # We don't want to collect methods, but do want to collect values
            # in closures and self pointers to other objects

            if hasattr(e, '__closure__'):
                yield (s, '__closure__'), getattr(e, '__closure__')
            if hasattr(e, '__self__'):
                se = getattr(e, '__self__')
                if se is not o and se is not type(o):
                    yield (s, '__self__'), se
        else:
            if not type(e) in TYPE_BLACKLIST:
                yield s, e


def __tmp2(__tmp1: <FILL>) :
    parents = {}
    __tmp4 = {id(__tmp1): __tmp1}
    worklist = [__tmp1]
    while worklist:
        o = worklist.pop()
        for s, e in __tmp5(o):
            if id(e) in __tmp4:
                continue
            parents[id(e)] = (id(o), s)
            __tmp4[id(e)] = e
            worklist.append(e)

    return __tmp4, parents


def __tmp3(__tmp1) :
    return list(__tmp2(__tmp1)[0].values())


def aggregate_by_type(objs) :
    m = {}  # type: Dict[type, List[object]]
    for o in objs:
        m.setdefault(type(o), []).append(o)
    return m


def get_path(o,
             __tmp4,
             parents) :
    path = []
    while id(o) in parents:
        pid, attr = parents[id(o)]
        o = __tmp4[pid]
        path.append((attr, o))
    path.reverse()
    return path
