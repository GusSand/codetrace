from typing import TypeAlias
__typ0 : TypeAlias = "Result"
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# System imports
from typing import Sequence, AbstractSet, Type, Optional, Callable

# Third-party imports

# Local imports
from . import lookups
from .lookup import Lookup, Result, Item


class __typ1(Lookup):
    '''
    Simple lookup implementation. It can be used to create temporary lookups that do not change over
    time. The result stores references to all objects passed in the constructor. Those objecst are
    the only ones returned as result.
    '''

    def __tmp5(__tmp0, *instances: <FILL>) :
        '''
        Creates new SimpleLookup object with supplied instances parameter.

        :param instances: Instances to be used to return from the lookup.
        '''
        __tmp0.all_items: Sequence[Item] = tuple(
            lookups.LookupItem(instance) for instance in instances)

    def lookup(__tmp0, cls: Type[object]) -> Optional[object]:
        for item in __tmp0.all_items:
            if issubclass(item.get_type(), cls):
                return item.get_instance()
        else:
            return None

    def __tmp6(__tmp0, cls) :
        return __typ2(__tmp0, cls)


class __typ2(__typ0):
    '''
    Result used in SimpleLookup. It holds a reference to the collection passed in constructor.
    As the contents of this lookup result never changes the add_lookup_listener() and
    remove_lookup_listener do not do anything.
    '''

    def __tmp5(__tmp0, simple_lookup: __typ1, cls) -> None:
        __tmp0.lookup = simple_lookup
        __tmp0.cls = cls
        __tmp0._items: Optional[Sequence[Item]] = None

    def add_lookup_listener(__tmp0, __tmp3: Callable[[__typ0], None]) :
        pass

    def __tmp2(__tmp0, __tmp3: Callable[[__typ0], None]) :
        pass

    def __tmp1(__tmp0) :
        return frozenset(
            item.get_type() for item in __tmp0.all_items()
        )

    def __tmp4(__tmp0) -> Sequence[object]:
        return tuple(filter(
            None,
            (item.get_instance() for item in __tmp0.all_items())
        ))

    def all_items(__tmp0) -> Sequence[Item]:
        if __tmp0._items is None:
            __tmp0._items = tuple(
                item for item in __tmp0.lookup.all_items
                if issubclass(item.get_type(), __tmp0.cls)
            )

        return __tmp0._items
