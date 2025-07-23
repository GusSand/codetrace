from typing import TypeAlias
__typ0 : TypeAlias = "Path"
from typing import NamedTuple, Dict
from frozendict import frozendict
from ...types import Path
from .base_handler import BaseHandler, ComplexFiller


class __typ1(ComplexFiller):
    form: frozendict
    __tmp3: __typ0
    original_value: frozendict


class ObjectHandler(BaseHandler[frozendict, __typ1, frozendict]):

    pathed_counter: Dict[tuple, int]
    __tmp0 = __typ1

    def __init__(__tmp1, *args, **kwargs):
        __tmp1.pathed_counter = {}
        super().__init__(*args, **kwargs)

    def __tmp4(__tmp1, __tmp3, value: <FILL>):
        __tmp1.pathed_counter[__tmp3] = 0
        clone = value.copy()
        for key, value in value.items():
            clone[key] = __tmp1.simplify_value(__tmp3 + (key,), value)

        return __tmp1.create_filler(frozendict, __tmp3, frozendict(clone))

    def __tmp2(__tmp1, __tmp3: __typ0, __tmp0: __typ1) :
        options = tuple(__tmp1.path_map[__tmp3][frozendict])
        original = options[__tmp1.pathed_counter[__tmp3]].original_value
        if __tmp1.pathed_counter[__tmp3] < len(options) - 1:
            __tmp1.pathed_counter[__tmp3] += 1

        out = {}
        for key, value in original.items():
            out[key] = __tmp1.realify_filler(__tmp3 + (key,), value)
        return out
