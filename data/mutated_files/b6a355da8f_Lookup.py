from typing import TypeAlias
__typ1 : TypeAlias = "Result"
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Provides a lookup that merge results from several lookups.
'''

# System imports
from itertools import chain
from typing import Sequence, MutableSequence, AbstractSet, Type, Optional, Callable
from weakref import WeakValueDictionary  # , WeakSet

# Third-party imports

# Local imports
from .lookup import Lookup, Item, Result
from .weak_observable import WeakCallable


class __typ0(Lookup):
    '''
    Implementation of a lookup that concile results from multiple lookups at the same time.
    '''

    def __init__(__tmp0, *lookups) :
        '''
        Creates a new ProxyLookup from an optional list of lookups to use as sources.

        :param lookups: Initial lookup sources.
        '''
        __tmp0._lookups = list(lookups)
        __tmp0._results: WeakValueDictionary[Type[object], PLResult] = WeakValueDictionary()

        super().__init__()

    def __tmp3(__tmp0, lookup: <FILL>) :
        '''
        Adds a lookup to the list of sources for the proxy.
        Will update all results accordingly
        '''
        __tmp0._lookups.append(lookup)
        for __tmp4 in __tmp0._results.values():
            __tmp4._lookup_added(lookup)

    def __tmp5(__tmp0, lookup) :
        '''
        Removes a lookup from the list of sources for the proxy.
        Will update all results accordingly
        '''
        __tmp0._lookups.remove(lookup)
        for __tmp4 in __tmp0._results.values():
            __tmp4._lookup_removed(lookup)

    def lookup(__tmp0, __tmp2) :
        for lookup in __tmp0._lookups:
            obj = lookup(__tmp2)
            if obj is not None:
                return obj
        else:
            return None

    def lookup_item(__tmp0, __tmp2) :
        for lookup in __tmp0._lookups:
            item = lookup.lookup_item(__tmp2)
            if item is not None:
                return item
        else:
            return None

    def lookup_result(__tmp0, __tmp2) :
        __tmp4 = __tmp0._results.get(__tmp2, None)
        if __tmp4 is not None:
            return __tmp4

        __tmp4 = PLResult(__tmp0, __tmp2)
        __tmp0._results[__tmp2] = __tmp4

        return __tmp4


class PLResult(__typ1):
    '''
    Implementation of a composite result that supports having multiple lookup sources.
    When _lookup_added() or _lookup_removed() are invoked (from ProxyLookup.add/remove_lookup()),
    listeners will be notified if instances appears or dissapears from the composite result.
    '''

    def __init__(__tmp0, lookup, __tmp2) -> None:
        __tmp0._lookup = lookup
        __tmp0._cls = __tmp2
        __tmp0._listeners: MutableSequence[WeakCallable] = []

        __tmp0._results = {
            lookup: lookup.lookup_result(__tmp2)
            for lookup in __tmp0._lookup._lookups
        }

    def _lookup_added(__tmp0, lookup) :
        __tmp4 = lookup.lookup_result(__tmp0._cls)
        __tmp0._results[lookup] = __tmp4

        if __tmp0._listeners:
            # If this new result already contains some instances, trigger the listeners.
            # Use all_classes() (that should internally use Item.get_type()) instead of
            # all_instances() to avoid loading instances of converted items.
            if __tmp4.all_classes():
                __tmp0._proxy_listener(__tmp4)

            __tmp4.add_lookup_listener(__tmp0._proxy_listener)

    def _lookup_removed(__tmp0, lookup: Lookup) :
        __tmp4 = __tmp0._results[lookup]

        if __tmp0._listeners:
            __tmp4.remove_lookup_listener(__tmp0._proxy_listener)

            # If this result contained some instances, trigger the listeners.
            # Use all_classes() (that should internally use Item.get_type()) instead of
            # all_instances() to avoid loading instances of converted items.
            if __tmp4.all_classes():
                __tmp0._proxy_listener(__tmp4)

        del __tmp0._results[lookup]
        del __tmp4

    def add_lookup_listener(__tmp0, __tmp1) :
        if not __tmp0._listeners:
            for __tmp4 in __tmp0._results.values():
                __tmp4.add_lookup_listener(__tmp0._proxy_listener)

        __tmp0._listeners.append(WeakCallable(__tmp1, __tmp0._listeners.remove))

    def remove_lookup_listener(__tmp0, __tmp1) -> None:
        __tmp0._listeners.remove(__tmp1)  # type: ignore

        if not __tmp0._listeners:
            for __tmp4 in __tmp0._results.values():
                __tmp4.remove_lookup_listener(__tmp0._proxy_listener)

    def _proxy_listener(__tmp0, __tmp4) :
        for __tmp1 in __tmp0._listeners:
            __tmp1(__tmp0)

    def all_classes(__tmp0) -> AbstractSet[Type[object]]:
        return frozenset(chain(*(
            __tmp4.all_classes()
            for __tmp4 in __tmp0._results.values()
        )))

    def all_instances(__tmp0) -> Sequence[object]:
        return tuple(chain(*(
            __tmp4.all_instances()
            for __tmp4 in __tmp0._results.values()
        )))

    def all_items(__tmp0) :
        return tuple(chain(*(
            __tmp4.all_items()
            for __tmp4 in __tmp0._results.values()
        )))
