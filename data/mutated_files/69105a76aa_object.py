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


def __tmp0(o, __tmp2) :
    return isinstance(getattr(type(o), __tmp2, None), property)


def get_edge_candidates(o: object) :
    if type(o) not in COLLECTION_TYPE_BLACKLIST:
        for __tmp2 in dir(o):
            if __tmp2 not in ATTR_BLACKLIST and hasattr(o, __tmp2) and not __tmp0(o, __tmp2):
                e = getattr(o, __tmp2)
                if not type(e) in ATOMIC_TYPE_BLACKLIST:
                    yield __tmp2, e
    if isinstance(o, Mapping):
        for k, v in o.items():
            yield k, v
    elif isinstance(o, Iterable) and not isinstance(o, str):
        for i, e in enumerate(o):
            yield i, e


def __tmp6(o: object) -> Iterator[Tuple[object, object]]:
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


def get_reachable_graph(root: object) -> Tuple[Dict[int, object],
                                               Dict[int, Tuple[int, object]]]:
    __tmp3 = {}
    __tmp5 = {id(root): root}
    worklist = [root]
    while worklist:
        o = worklist.pop()
        for s, e in __tmp6(o):
            if id(e) in __tmp5:
                continue
            __tmp3[id(e)] = (id(o), s)
            __tmp5[id(e)] = e
            worklist.append(e)

    return __tmp5, __tmp3


def __tmp4(root: <FILL>) :
    return list(get_reachable_graph(root)[0].values())


def __tmp1(objs: List[object]) -> Dict[type, List[object]]:
    m = {}  # type: Dict[type, List[object]]
    for o in objs:
        m.setdefault(type(o), []).append(o)
    return m


def get_path(o: object,
             __tmp5: Dict[int, object],
             __tmp3) :
    path = []
    while id(o) in __tmp3:
        pid, __tmp2 = __tmp3[id(o)]
        o = __tmp5[pid]
        path.append((__tmp2, o))
    path.reverse()
    return path
