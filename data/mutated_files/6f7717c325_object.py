from typing import TypeAlias
__typ3 : TypeAlias = "Lookup"
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
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


def singleton(member, id_: __typ1 = None) :
    return singleton_module.SingletonLookup(member, id_)


def fixed(*members: object) :
    if not members:
        return EmptyLookup()

    elif len(members) == 1:
        return singleton(members[0])

    else:
        return simple.SimpleLookup(*members)


class __typ2(Result):

    def add_lookup_listener(self, listener: Callable[[Result], None]) :
        pass

    def remove_lookup_listener(self, listener) :
        pass

    def all_classes(self) :
        return frozenset()

    def all_instances(self) -> Sequence[object]:
        return tuple()

    def all_items(self) :
        return tuple()


class EmptyLookup(__typ3):

    NO_RESULT = __typ2()

    def lookup(self, cls: Type[object]) :
        return None

    def lookup_result(self, cls: Type[object]) -> Result:
        return self.NO_RESULT


class __typ4(Item):

    def __tmp1(self, instance: object, id_: __typ1 = None) -> None:
        if instance is None:
            raise ValueError('None cannot be a lookup member')

        self._instance = instance
        self._id = id_

    def __tmp0(self) :
        return self.get_id()

    def get_id(self) :
        if self._id is not None:
            return self._id
        else:
            return __typ1(self._instance)

    def get_instance(self) -> Optional[object]:
        return self._instance

    def get_type(self) -> Type[object]:
        return type(self._instance)

    def __eq__(self, other: <FILL>) -> bool:
        if isinstance(other, type(self)):
            return self._instance == other.get_instance()
        else:
            return False

    def __hash__(self) -> __typ0:
        try:
            return hash(self._instance)
        except TypeError:  # Mutable, cannot be hashed
            return id(self._instance)
