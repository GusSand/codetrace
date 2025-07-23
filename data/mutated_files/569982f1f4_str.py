from typing import TypeAlias
__typ1 : TypeAlias = "object"
__typ0 : TypeAlias = "bool"
"""Find all objects reachable from a root object."""

from collections import deque
from collections.abc import Iterable
from typing import List, Dict, Iterator, Optional, Tuple, Mapping
import weakref
import types


method_descriptor_type = type(__typ1.__dir__)
method_wrapper_type = type(__typ1().__ne__)
wrapper_descriptor_type = type(__typ1.__ne__)

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
    __typ1,
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


def isproperty(o, attr: <FILL>) :
    return isinstance(getattr(type(o), attr, None), property)


def get_edge_candidates(o) -> Iterator[Tuple[__typ1, __typ1]]:
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


def __tmp7(o: __typ1) -> Iterator[Tuple[__typ1, __typ1]]:
    for s, e in get_edge_candidates(o):
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


def __tmp3(__tmp2: __typ1) -> Tuple[Dict[int, __typ1],
                                               Dict[int, Tuple[int, __typ1]]]:
    __tmp4 = {}
    __tmp6 = {id(__tmp2): __tmp2}
    worklist = [__tmp2]
    while worklist:
        o = worklist.pop()
        for s, e in __tmp7(o):
            if id(e) in __tmp6:
                continue
            __tmp4[id(e)] = (id(o), s)
            __tmp6[id(e)] = e
            worklist.append(e)

    return __tmp6, __tmp4


def __tmp5(__tmp2) -> List[__typ1]:
    return list(__tmp3(__tmp2)[0].values())


def __tmp0(objs) -> Dict[type, List[__typ1]]:
    m = {}  # type: Dict[type, List[object]]
    for o in objs:
        m.setdefault(type(o), []).append(o)
    return m


def __tmp1(o,
             __tmp6,
             __tmp4) :
    path = []
    while id(o) in __tmp4:
        pid, attr = __tmp4[id(o)]
        o = __tmp6[pid]
        path.append((attr, o))
    path.reverse()
    return path
