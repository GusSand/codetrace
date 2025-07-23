from typing import NamedTuple, Dict, Any
from enum import Enum, auto
from collections import defaultdict
from frozendict import frozendict
from ...types import Path
from .base_handler import BaseHandler, ComplexFiller


class ArrayForms(Enum):
    EMPTY = auto()
    FILLED = auto()


class ArrayFiller(ComplexFiller):
    form: ArrayForms
    path: Path
    original_value: tuple


class ArrayHandler(BaseHandler[tuple, ArrayFiller, ArrayForms]):

    pathed_counter: Dict[tuple, int]
    pathed_types: Dict[tuple, set]

    filler = ArrayFiller

    def __init__(__tmp1, *args, **kwargs):
        __tmp1.pathed_counter = {}
        __tmp1.pathed_types = defaultdict(set)
        super().__init__(*args, **kwargs)

    def simplify(__tmp1, path, __tmp0: <FILL>):
        if len(__tmp0) == 0:
            return __tmp1.create_filler(ArrayForms.EMPTY, path, ())

        items = set()
        for index, item in enumerate(__tmp0):
            items.add(__tmp1.simplify_value(path, item))
        items = tuple(items)

        __tmp1.pathed_counter[path] = 0
        __tmp1.pathed_types[path].add(items)

        return __tmp1.create_filler(ArrayForms.FILLED, path, items)

    def __tmp2(__tmp1, path, filler) :
        if filler.form == ArrayForms.EMPTY:
            return []

        options = tuple(__tmp1.pathed_types[path])

        out = []
        for i, option in enumerate(options[__tmp1.pathed_counter[path]]):
            out.append(__tmp1.realify_filler(path, option))

        if __tmp1.pathed_counter[path] < len(options) - 1:
            __tmp1.pathed_counter[path] += 1
        return out
