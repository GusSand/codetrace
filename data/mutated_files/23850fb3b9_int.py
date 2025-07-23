from typing import TypeAlias
__typ2 : TypeAlias = "object"
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

    def __tmp4(__tmp0) :
        __tmp0._content: Collection[GL.Pair] = set()

        # Do not serialize
        __tmp0._results: WeakValueDictionary[Type[__typ2], GL.GLResult] = WeakValueDictionary()

    def __tmp1(__tmp0, __tmp2: int) :
        return __typ0(__tmp2, __tmp0._content)

    def end_transaction(__tmp0, transaction) :
        __tmp0._content, change_set = transaction.new_content(__tmp0._content)

        results_to_notify = set()
        for __tmp5 in change_set:
            cls = __tmp5.get_type()
            for result_type, __tmp3 in __tmp0._results.items():
                if issubclass(cls, result_type):
                    results_to_notify.add(__tmp3)
                    __tmp3.clear_cache()

        return results_to_notify

    def lookup(__tmp0, cls) :
        for __tmp5 in __tmp0._content:  # TODO: improve
            if issubclass(__tmp5.get_type(), cls):
                yield __tmp5

    def register_result(__tmp0, __tmp3: GL.GLResult) -> None:
        __tmp0._results[__tmp3._cls] = __tmp3

    def find_result(__tmp0, cls) -> Optional[GL.GLResult]:
        return __tmp0._results.get(cls, None)

    def __contains__(__tmp0, item: __typ2) -> bool:
        return item in __tmp0._content


class __typ0(GL.Transaction):

    def __tmp4(__tmp0, __tmp2: <FILL>, current_content) -> None:
        __tmp0._new_list = set(current_content)
        __tmp0._changed: Set[GL.Pair] = set()

    def new_content(__tmp0, prev) -> Tuple[Collection[GL.Pair], Set[GL.Pair]]:
        return __tmp0._new_list, __tmp0._changed

    def add(__tmp0, __tmp5) -> bool:
        not_present = __tmp5 not in __tmp0._new_list
        if not_present:
            __tmp0._changed.add(__tmp5)
        __tmp0._new_list.add(__tmp5)
        return not_present

    def remove(__tmp0, __tmp5) -> None:
        __tmp0._changed.add(__tmp5)
        __tmp0._new_list.remove(__tmp5)

    def set_all(__tmp0, pairs: Collection[GL.Pair]) -> None:
        pairs = set(pairs)
        __tmp0._changed.update(pairs.symmetric_difference(__tmp0._new_list))
        __tmp0._new_list = pairs
