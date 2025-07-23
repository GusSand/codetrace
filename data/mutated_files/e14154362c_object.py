# -*- coding: utf-8 -*-
# Copyright (c) 2019 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Static factory methods for creating common lookup implementations.
'''

# System imports
from typing import Sequence, AbstractSet, Type, Optional, Callable

# Third-party imports

# Local imports
from . import singleton as singleton_module, simple
from .lookup import Lookup, Item, Result


def singleton(__tmp6: <FILL>, id_: str = None) -> Lookup:
    return singleton_module.SingletonLookup(__tmp6, id_)


def __tmp12(*members: object) -> Lookup:
    if not members:
        return EmptyLookup()

    elif len(members) == 1:
        return singleton(members[0])

    else:
        return simple.SimpleLookup(*members)


class NoResult(Result):

    def __tmp15(__tmp1, __tmp7: Callable[[Result], None]) -> None:
        pass

    def __tmp4(__tmp1, __tmp7: Callable[[Result], None]) :
        pass

    def __tmp3(__tmp1) :
        return frozenset()

    def all_instances(__tmp1) :
        return tuple()

    def __tmp13(__tmp1) -> Sequence[Item]:
        return tuple()


class EmptyLookup(Lookup):

    NO_RESULT = NoResult()

    def lookup(__tmp1, __tmp9: Type[object]) -> Optional[object]:
        return None

    def __tmp14(__tmp1, __tmp9: Type[object]) -> Result:
        return __tmp1.NO_RESULT


class LookupItem(Item):

    def __init__(__tmp1, __tmp5, id_: str = None) -> None:
        if __tmp5 is None:
            raise ValueError('None cannot be a lookup member')

        __tmp1._instance = __tmp5
        __tmp1._id = id_

    def __tmp11(__tmp1) -> str:
        return __tmp1.get_id()

    def get_id(__tmp1) -> str:
        if __tmp1._id is not None:
            return __tmp1._id
        else:
            return str(__tmp1._instance)

    def get_instance(__tmp1) -> Optional[object]:
        return __tmp1._instance

    def __tmp0(__tmp1) -> Type[object]:
        return type(__tmp1._instance)

    def __tmp2(__tmp1, __tmp10) -> bool:
        if isinstance(__tmp10, type(__tmp1)):
            return __tmp1._instance == __tmp10.get_instance()
        else:
            return False

    def __tmp8(__tmp1) -> int:
        try:
            return hash(__tmp1._instance)
        except TypeError:  # Mutable, cannot be hashed
            return id(__tmp1._instance)
