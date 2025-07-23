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


def __tmp1(o: object, attr: str) -> bool:
    return isinstance(getattr(type(o), attr, None), property)


def __tmp2(o: object) :
    if type(o) not in COLLECTION_TYPE_BLACKLIST:
        for attr in dir(o):
            if attr not in ATTR_BLACKLIST and hasattr(o, attr) and not __tmp1(o, attr):
                e = getattr(o, attr)
                if not type(e) in ATOMIC_TYPE_BLACKLIST:
                    yield attr, e
    if isinstance(o, Mapping):
        for k, v in o.items():
            yield k, v
    elif isinstance(o, Iterable) and not isinstance(o, str):
        for i, e in enumerate(o):
            yield i, e


def __tmp7(o: <FILL>) -> Iterator[Tuple[object, object]]:
    for s, e in __tmp2(o):
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


def get_reachable_graph(__tmp5: object) -> Tuple[Dict[int, object],
                                               Dict[int, Tuple[int, object]]]:
    parents = {}
    seen = {id(__tmp5): __tmp5}
    worklist = [__tmp5]
    while worklist:
        o = worklist.pop()
        for s, e in __tmp7(o):
            if id(e) in seen:
                continue
            parents[id(e)] = (id(o), s)
            seen[id(e)] = e
            worklist.append(e)

    return seen, parents


def __tmp6(__tmp5: object) -> List[object]:
    return list(get_reachable_graph(__tmp5)[0].values())


def __tmp3(__tmp0: List[object]) -> Dict[type, List[object]]:
    m = {}  # type: Dict[type, List[object]]
    for o in __tmp0:
        m.setdefault(type(o), []).append(o)
    return m


def __tmp4(o: object,
             seen: Dict[int, object],
             parents: Dict[int, Tuple[int, object]]) -> List[Tuple[object, object]]:
    path = []
    while id(o) in parents:
        pid, attr = parents[id(o)]
        o = seen[pid]
        path.append((attr, o))
    path.reverse()
    return path
