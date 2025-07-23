from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ2 : TypeAlias = "str"
__typ4 : TypeAlias = "bool"
__typ6 : TypeAlias = "Result"
__typ3 : TypeAlias = "Lookup"
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


def singleton(__tmp5, id_: __typ2 = None) -> __typ3:
    return singleton_module.SingletonLookup(__tmp5, id_)


def fixed(*members: <FILL>) :
    if not members:
        return __typ1()

    elif len(members) == 1:
        return singleton(members[0])

    else:
        return simple.SimpleLookup(*members)


class NoResult(__typ6):

    def __tmp12(__tmp1, __tmp4) :
        pass

    def remove_lookup_listener(__tmp1, __tmp4) :
        pass

    def __tmp3(__tmp1) :
        return frozenset()

    def all_instances(__tmp1) :
        return tuple()

    def __tmp10(__tmp1) -> Sequence[Item]:
        return tuple()


class __typ1(__typ3):

    NO_RESULT = NoResult()

    def lookup(__tmp1, __tmp6) :
        return None

    def __tmp11(__tmp1, __tmp6) :
        return __tmp1.NO_RESULT


class __typ5(Item):

    def __tmp9(__tmp1, instance, id_: __typ2 = None) :
        if instance is None:
            raise ValueError('None cannot be a lookup member')

        __tmp1._instance = instance
        __tmp1._id = id_

    def __tmp8(__tmp1) :
        return __tmp1.get_id()

    def get_id(__tmp1) :
        if __tmp1._id is not None:
            return __tmp1._id
        else:
            return __typ2(__tmp1._instance)

    def get_instance(__tmp1) :
        return __tmp1._instance

    def __tmp0(__tmp1) -> Type[object]:
        return type(__tmp1._instance)

    def __tmp2(__tmp1, __tmp7) :
        if isinstance(__tmp7, type(__tmp1)):
            return __tmp1._instance == __tmp7.get_instance()
        else:
            return False

    def __hash__(__tmp1) :
        try:
            return hash(__tmp1._instance)
        except TypeError:  # Mutable, cannot be hashed
            return id(__tmp1._instance)
