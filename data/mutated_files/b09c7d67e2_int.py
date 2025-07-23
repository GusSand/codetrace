from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "object"
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# System imports
from typing import Iterable, Collection, Set, Type, Optional, Tuple
from weakref import WeakValueDictionary

# Third-party imports

# Local imports
from . import generic_lookup as GL


class __typ1(GL.Storage):
    '''Storing Pairs in a set datastructure, for GenericLookup.'''

    def __tmp7(__tmp0) -> None:
        __tmp0._content: Collection[GL.Pair] = set()

        # Do not serialize
        __tmp0._results: WeakValueDictionary[Type[__typ3], GL.GLResult] = WeakValueDictionary()

    def __tmp1(__tmp0, ensure: <FILL>) -> GL.Transaction:
        return __typ0(ensure, __tmp0._content)

    def __tmp3(__tmp0, __tmp11: GL.Transaction) -> Iterable[GL.GLResult]:
        __tmp0._content, change_set = __tmp11.new_content(__tmp0._content)

        results_to_notify = set()
        for __tmp10 in change_set:
            __tmp5 = __tmp10.get_type()
            for result_type, __tmp6 in __tmp0._results.items():
                if issubclass(__tmp5, result_type):
                    results_to_notify.add(__tmp6)
                    __tmp6.clear_cache()

        return results_to_notify

    def lookup(__tmp0, __tmp5: Type[__typ3]) -> Iterable[GL.Pair]:
        for __tmp10 in __tmp0._content:  # TODO: improve
            if issubclass(__tmp10.get_type(), __tmp5):
                yield __tmp10

    def register_result(__tmp0, __tmp6: GL.GLResult) :
        __tmp0._results[__tmp6._cls] = __tmp6

    def __tmp9(__tmp0, __tmp5: Type[__typ3]) -> Optional[GL.GLResult]:
        return __tmp0._results.get(__tmp5, None)

    def __contains__(__tmp0, __tmp2: __typ3) -> __typ2:
        return __tmp2 in __tmp0._content


class __typ0(GL.Transaction):

    def __tmp7(__tmp0, ensure: int, __tmp8: Collection[GL.Pair]) -> None:
        __tmp0._new_list = set(__tmp8)
        __tmp0._changed: Set[GL.Pair] = set()

    def new_content(__tmp0, __tmp4: Collection[GL.Pair]) -> Tuple[Collection[GL.Pair], Set[GL.Pair]]:
        return __tmp0._new_list, __tmp0._changed

    def add(__tmp0, __tmp10: GL.Pair) -> __typ2:
        not_present = __tmp10 not in __tmp0._new_list
        if not_present:
            __tmp0._changed.add(__tmp10)
        __tmp0._new_list.add(__tmp10)
        return not_present

    def remove(__tmp0, __tmp10: GL.Pair) -> None:
        __tmp0._changed.add(__tmp10)
        __tmp0._new_list.remove(__tmp10)

    def set_all(__tmp0, pairs: Collection[GL.Pair]) -> None:
        pairs = set(pairs)
        __tmp0._changed.update(pairs.symmetric_difference(__tmp0._new_list))
        __tmp0._new_list = pairs
