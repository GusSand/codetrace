from typing import TypeAlias
__typ1 : TypeAlias = "dict"
from typing import NamedTuple, Dict
from frozendict import frozendict
from ...types import Path
from .base_handler import BaseHandler, ComplexFiller


class __typ2(ComplexFiller):
    form: frozendict
    path: Path
    original_value: frozendict


class __typ0(BaseHandler[frozendict, __typ2, frozendict]):

    pathed_counter: Dict[tuple, int]
    __tmp0 = __typ2

    def __init__(__tmp1, *args, **kwargs):
        __tmp1.pathed_counter = {}
        super().__init__(*args, **kwargs)

    def __tmp4(__tmp1, path: <FILL>, __tmp3):
        __tmp1.pathed_counter[path] = 0
        clone = __tmp3.copy()
        for key, __tmp3 in __tmp3.items():
            clone[key] = __tmp1.simplify_value(path + (key,), __tmp3)

        return __tmp1.create_filler(frozendict, path, frozendict(clone))

    def __tmp2(__tmp1, path, __tmp0) :
        options = tuple(__tmp1.path_map[path][frozendict])
        original = options[__tmp1.pathed_counter[path]].original_value
        if __tmp1.pathed_counter[path] < len(options) - 1:
            __tmp1.pathed_counter[path] += 1

        out = {}
        for key, __tmp3 in original.items():
            out[key] = __tmp1.realify_filler(path + (key,), __tmp3)
        return out
