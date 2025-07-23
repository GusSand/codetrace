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
    bool,
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


def __tmp1(o: object, __tmp4: str) -> bool:
    return isinstance(getattr(type(o), __tmp4, None), property)


def get_edge_candidates(o: object) -> Iterator[Tuple[object, object]]:
    if type(o) not in COLLECTION_TYPE_BLACKLIST:
        for __tmp4 in dir(o):
            if __tmp4 not in ATTR_BLACKLIST and hasattr(o, __tmp4) and not __tmp1(o, __tmp4):
                e = getattr(o, __tmp4)
                if not type(e) in ATOMIC_TYPE_BLACKLIST:
                    yield __tmp4, e
    if isinstance(o, Mapping):
        for k, v in o.items():
            yield k, v
    elif isinstance(o, Iterable) and not isinstance(o, str):
        for i, e in enumerate(o):
            yield i, e


def __tmp7(o) :
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


def __tmp5(__tmp3) -> Tuple[Dict[int, object],
                                               Dict[int, Tuple[int, object]]]:
    parents = {}
    __tmp6 = {id(__tmp3): __tmp3}
    worklist = [__tmp3]
    while worklist:
        o = worklist.pop()
        for s, e in __tmp7(o):
            if id(e) in __tmp6:
                continue
            parents[id(e)] = (id(o), s)
            __tmp6[id(e)] = e
            worklist.append(e)

    return __tmp6, parents


def find_all_reachable(__tmp3: object) :
    return list(__tmp5(__tmp3)[0].values())


def aggregate_by_type(__tmp0: List[object]) -> Dict[type, List[object]]:
    m = {}  # type: Dict[type, List[object]]
    for o in __tmp0:
        m.setdefault(type(o), []).append(o)
    return m


def __tmp2(o: <FILL>,
             __tmp6: Dict[int, object],
             parents) :
    path = []
    while id(o) in parents:
        pid, __tmp4 = parents[id(o)]
        o = __tmp6[pid]
        path.append((__tmp4, o))
    path.reverse()
    return path
