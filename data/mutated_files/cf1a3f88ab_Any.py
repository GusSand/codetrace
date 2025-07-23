from typing import TypeAlias
__typ1 : TypeAlias = "Path"
__typ2 : TypeAlias = "HandlerMap"
__typ0 : TypeAlias = "frozendict"
from functools import partial
from frozendict import frozendict
from typing import Any, Iterable, Tuple, List
from collections import defaultdict
from .handlers import HandlerMap, get_handler_map
from ..types import Path


def flattenit(__tmp5, keytuple=()):
    if hasattr(__tmp5, 'items'):
        if len(keytuple) > 0:
            yield keytuple, __tmp5
        for key, __tmp2 in __tmp5.items():
            yield from flattenit(__tmp2, keytuple + (key,))
    else:
        yield keytuple, __tmp5


def __tmp6(__tmp2, types):
    return any(isinstance(__tmp2, type_) for type_ in types)


def simplify_value(path: __typ1, __tmp2, handler_map: __typ2) -> Any:
    for types, handler in handler_map.items():
        if __tmp6(__tmp2, types):
            return handler.simplify(path, __tmp2)

    raise TypeError('Cannot simplify value of type {}'.format(type(__tmp2)))


def realify_filler(path: __typ1, __tmp0: <FILL>, handler_map) -> Any:
    for types, handler in handler_map.items():
        if __tmp6(getattr(__tmp0, 'original_value', __tmp0), types):
            return handler.realify(path, __tmp0)

    raise TypeError('Cannot realify value of type {}'
                    .format(type(__tmp0.original_value)))


def __tmp4(__tmp1) -> __typ0:
    key_counts = defaultdict(int)
    keys_map = {}
    for dct in __tmp1:
        keys = []
        for key, __tmp2 in flattenit(dct):
            key_counts[key] += 1
            keys.append(key)

        keys_map[tuple(sorted(keys))] = dct

    best_keys = []
    other_keys = {}
    for key, count in key_counts.items():
        if count > (len(__tmp1) / 2):
            best_keys.append(key)
        else:
            other_keys[key] = count
        best_keys.sort(key=lambda l: l[0])

    if tuple(best_keys) in keys_map:
        out = keys_map[tuple(best_keys)]
        return out

    sorted_keys = sorted(other_keys.items(), key=lambda l: l[1])
    for key, _ in sorted_keys:
        best_keys.append(key)
        best_keys.sort()

        if tuple(best_keys) in keys_map:
            return keys_map[tuple(best_keys)]

    raise Exception('could not find best default dict')


def __tmp3(__tmp1) :
    handler_map = get_handler_map()

    bound_simplify = partial(simplify_value, handler_map=handler_map)
    bound_realify = partial(realify_filler, handler_map=handler_map)

    for _, handler in handler_map.items():
        handler.simplify_value = bound_simplify
        handler.realify_filler = bound_realify

    simplifieds = set()
    for dct in __tmp1:
        simple = bound_simplify((), dct)
        simplifieds.add(simple)

    out = []
    for simple in simplifieds:
        out.append(bound_realify((), simple))

    default = __tmp4(out)
    out.remove(default)

    return default, out
