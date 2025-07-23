from typing import TypeAlias
__typ3 : TypeAlias = "tuple"
__typ2 : TypeAlias = "list"
from typing import NamedTuple, Dict, Any
from enum import Enum, auto
from collections import defaultdict
from frozendict import frozendict
from ...types import Path
from .base_handler import BaseHandler, ComplexFiller


class __typ4(Enum):
    EMPTY = auto()
    FILLED = auto()


class __typ1(ComplexFiller):
    form: __typ4
    path: Path
    original_value: __typ3


class __typ0(BaseHandler[__typ3, __typ1, __typ4]):

    pathed_counter: Dict[__typ3, int]
    pathed_types: Dict[__typ3, set]

    __tmp0 = __typ1

    def __init__(__tmp1, *args, **kwargs):
        __tmp1.pathed_counter = {}
        __tmp1.pathed_types = defaultdict(set)
        super().__init__(*args, **kwargs)

    def simplify(__tmp1, path, value):
        if len(value) == 0:
            return __tmp1.create_filler(__typ4.EMPTY, path, ())

        items = set()
        for index, item in enumerate(value):
            items.add(__tmp1.simplify_value(path, item))
        items = __typ3(items)

        __tmp1.pathed_counter[path] = 0
        __tmp1.pathed_types[path].add(items)

        return __tmp1.create_filler(__typ4.FILLED, path, items)

    def realify(__tmp1, path: <FILL>, __tmp0) :
        if __tmp0.form == __typ4.EMPTY:
            return []

        options = __typ3(__tmp1.pathed_types[path])

        out = []
        for i, option in enumerate(options[__tmp1.pathed_counter[path]]):
            out.append(__tmp1.realify_filler(path, option))

        if __tmp1.pathed_counter[path] < len(options) - 1:
            __tmp1.pathed_counter[path] += 1
        return out
