from typing import TypeAlias
__typ1 : TypeAlias = "int"
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


def singleton(__tmp3, id_: str = None) :
    return singleton_module.SingletonLookup(__tmp3, id_)


def __tmp6(*members) :
    if not members:
        return __typ0()

    elif len(members) == 1:
        return singleton(members[0])

    else:
        return simple.SimpleLookup(*members)


class NoResult(Result):

    def add_lookup_listener(__tmp0, __tmp2) :
        pass

    def remove_lookup_listener(__tmp0, __tmp2) :
        pass

    def __tmp1(__tmp0) :
        return frozenset()

    def all_instances(__tmp0) :
        return tuple()

    def all_items(__tmp0) :
        return tuple()


class __typ0(Lookup):

    NO_RESULT = NoResult()

    def lookup(__tmp0, __tmp4) :
        return None

    def __tmp7(__tmp0, __tmp4) :
        return __tmp0.NO_RESULT


class LookupItem(Item):

    def __init__(__tmp0, instance: <FILL>, id_: str = None) :
        if instance is None:
            raise ValueError('None cannot be a lookup member')

        __tmp0._instance = instance
        __tmp0._id = id_

    def get_display_name(__tmp0) :
        return __tmp0.get_id()

    def get_id(__tmp0) -> str:
        if __tmp0._id is not None:
            return __tmp0._id
        else:
            return str(__tmp0._instance)

    def get_instance(__tmp0) :
        return __tmp0._instance

    def get_type(__tmp0) :
        return type(__tmp0._instance)

    def __eq__(__tmp0, __tmp5) :
        if isinstance(__tmp5, type(__tmp0)):
            return __tmp0._instance == __tmp5.get_instance()
        else:
            return False

    def __hash__(__tmp0) :
        try:
            return hash(__tmp0._instance)
        except TypeError:  # Mutable, cannot be hashed
            return id(__tmp0._instance)
