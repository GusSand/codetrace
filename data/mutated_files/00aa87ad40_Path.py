from typing import TypeAlias
__typ2 : TypeAlias = "list"
from typing import NamedTuple, Dict, Any
from enum import Enum, auto
from collections import defaultdict
from frozendict import frozendict
from ...types import Path
from .base_handler import BaseHandler, ComplexFiller


class __typ1(Enum):
    EMPTY = auto()
    FILLED = auto()


class ArrayFiller(ComplexFiller):
    form: __typ1
    __tmp4: Path
    original_value: tuple


class __typ0(BaseHandler[tuple, ArrayFiller, __typ1]):

    pathed_counter: Dict[tuple, int]
    pathed_types: Dict[tuple, set]

    __tmp0 = ArrayFiller

    def __init__(__tmp1, *args, **kwargs):
        __tmp1.pathed_counter = {}
        __tmp1.pathed_types = defaultdict(set)
        super().__init__(*args, **kwargs)

    def __tmp5(__tmp1, __tmp4: <FILL>, __tmp3: tuple):
        if len(__tmp3) == 0:
            return __tmp1.create_filler(__typ1.EMPTY, __tmp4, ())

        items = set()
        for index, item in enumerate(__tmp3):
            items.add(__tmp1.simplify_value(__tmp4, item))
        items = tuple(items)

        __tmp1.pathed_counter[__tmp4] = 0
        __tmp1.pathed_types[__tmp4].add(items)

        return __tmp1.create_filler(__typ1.FILLED, __tmp4, items)

    def __tmp2(__tmp1, __tmp4, __tmp0) -> __typ2:
        if __tmp0.form == __typ1.EMPTY:
            return []

        options = tuple(__tmp1.pathed_types[__tmp4])

        out = []
        for i, option in enumerate(options[__tmp1.pathed_counter[__tmp4]]):
            out.append(__tmp1.realify_filler(__tmp4, option))

        if __tmp1.pathed_counter[__tmp4] < len(options) - 1:
            __tmp1.pathed_counter[__tmp4] += 1
        return out
