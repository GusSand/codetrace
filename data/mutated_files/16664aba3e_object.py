from typing import TypeAlias
__typ0 : TypeAlias = "int"
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


class SetStorage(GL.Storage):
    '''Storing Pairs in a set datastructure, for GenericLookup.'''

    def __tmp7(__tmp0) :
        __tmp0._content: Collection[GL.Pair] = set()

        # Do not serialize
        __tmp0._results: WeakValueDictionary[Type[object], GL.GLResult] = WeakValueDictionary()

    def __tmp5(__tmp0, __tmp3) -> GL.Transaction:
        return SetTransaction(__tmp3, __tmp0._content)

    def end_transaction(__tmp0, __tmp10) :
        __tmp0._content, change_set = __tmp10.new_content(__tmp0._content)

        results_to_notify = set()
        for __tmp9 in change_set:
            __tmp6 = __tmp9.get_type()
            for result_type, result in __tmp0._results.items():
                if issubclass(__tmp6, result_type):
                    results_to_notify.add(result)
                    result.clear_cache()

        return results_to_notify

    def lookup(__tmp0, __tmp6) :
        for __tmp9 in __tmp0._content:  # TODO: improve
            if issubclass(__tmp9.get_type(), __tmp6):
                yield __tmp9

    def register_result(__tmp0, result) :
        __tmp0._results[result._cls] = result

    def __tmp8(__tmp0, __tmp6: Type[object]) :
        return __tmp0._results.get(__tmp6, None)

    def __contains__(__tmp0, __tmp2: <FILL>) -> bool:
        return __tmp2 in __tmp0._content


class SetTransaction(GL.Transaction):

    def __tmp7(__tmp0, __tmp3, current_content: Collection[GL.Pair]) :
        __tmp0._new_list = set(current_content)
        __tmp0._changed: Set[GL.Pair] = set()

    def new_content(__tmp0, prev: Collection[GL.Pair]) -> Tuple[Collection[GL.Pair], Set[GL.Pair]]:
        return __tmp0._new_list, __tmp0._changed

    def add(__tmp0, __tmp9: GL.Pair) :
        not_present = __tmp9 not in __tmp0._new_list
        if not_present:
            __tmp0._changed.add(__tmp9)
        __tmp0._new_list.add(__tmp9)
        return not_present

    def remove(__tmp0, __tmp9) -> None:
        __tmp0._changed.add(__tmp9)
        __tmp0._new_list.remove(__tmp9)

    def __tmp1(__tmp0, __tmp4: Collection[GL.Pair]) -> None:
        __tmp4 = set(__tmp4)
        __tmp0._changed.update(__tmp4.symmetric_difference(__tmp0._new_list))
        __tmp0._new_list = __tmp4
