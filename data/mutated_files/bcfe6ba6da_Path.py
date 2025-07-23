from typing import TypeAlias
__typ0 : TypeAlias = "dict"
from typing import NamedTuple, Dict
from frozendict import frozendict
from ...types import Path
from .base_handler import BaseHandler, ComplexFiller


class __typ1(ComplexFiller):
    form: frozendict
    path: Path
    original_value: frozendict


class ObjectHandler(BaseHandler[frozendict, __typ1, frozendict]):

    pathed_counter: Dict[tuple, int]
    filler = __typ1

    def __init__(self, *args, **kwargs):
        self.pathed_counter = {}
        super().__init__(*args, **kwargs)

    def __tmp1(self, path, value: __typ0):
        self.pathed_counter[path] = 0
        clone = value.copy()
        for key, value in value.items():
            clone[key] = self.simplify_value(path + (key,), value)

        return self.create_filler(frozendict, path, frozendict(clone))

    def __tmp0(self, path: <FILL>, filler: __typ1) -> __typ0:
        options = tuple(self.path_map[path][frozendict])
        original = options[self.pathed_counter[path]].original_value
        if self.pathed_counter[path] < len(options) - 1:
            self.pathed_counter[path] += 1

        out = {}
        for key, value in original.items():
            out[key] = self.realify_filler(path + (key,), value)
        return out
