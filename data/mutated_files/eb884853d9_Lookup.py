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

    def __init__(__tmp0, *lookups: Lookup) :
        '''
        Creates a new ProxyLookup from an optional list of lookups to use as sources.

        :param lookups: Initial lookup sources.
        '''
        __tmp0._lookups = list(lookups)
        __tmp0._results: WeakValueDictionary[Type[object], PLResult] = WeakValueDictionary()

        super().__init__()

    def add_lookup(__tmp0, lookup: Lookup) -> None:
        '''
        Adds a lookup to the list of sources for the proxy.
        Will update all results accordingly
        '''
        __tmp0._lookups.append(lookup)
        for result in __tmp0._results.values():
            result._lookup_added(lookup)

    def remove_lookup(__tmp0, lookup: Lookup) -> None:
        '''
        Removes a lookup from the list of sources for the proxy.
        Will update all results accordingly
        '''
        __tmp0._lookups.remove(lookup)
        for result in __tmp0._results.values():
            result._lookup_removed(lookup)

    def lookup(__tmp0, __tmp1: Type[object]) :
        for lookup in __tmp0._lookups:
            obj = lookup(__tmp1)
            if obj is not None:
                return obj
        else:
            return None

    def lookup_item(__tmp0, __tmp1: Type[object]) -> Optional[Item]:
        for lookup in __tmp0._lookups:
            item = lookup.lookup_item(__tmp1)
            if item is not None:
                return item
        else:
            return None

    def lookup_result(__tmp0, __tmp1: Type[object]) -> Result:
        result = __tmp0._results.get(__tmp1, None)
        if result is not None:
            return result

        result = PLResult(__tmp0, __tmp1)
        __tmp0._results[__tmp1] = result

        return result


class PLResult(Result):
    '''
    Implementation of a composite result that supports having multiple lookup sources.
    When _lookup_added() or _lookup_removed() are invoked (from ProxyLookup.add/remove_lookup()),
    listeners will be notified if instances appears or dissapears from the composite result.
    '''

    def __init__(__tmp0, lookup: __typ0, __tmp1: Type[object]) -> None:
        __tmp0._lookup = lookup
        __tmp0._cls = __tmp1
        __tmp0._listeners: MutableSequence[WeakCallable] = []

        __tmp0._results = {
            lookup: lookup.lookup_result(__tmp1)
            for lookup in __tmp0._lookup._lookups
        }

    def _lookup_added(__tmp0, lookup: <FILL>) -> None:
        result = lookup.lookup_result(__tmp0._cls)
        __tmp0._results[lookup] = result

        if __tmp0._listeners:
            # If this new result already contains some instances, trigger the listeners.
            # Use all_classes() (that should internally use Item.get_type()) instead of
            # all_instances() to avoid loading instances of converted items.
            if result.all_classes():
                __tmp0._proxy_listener(result)

            result.add_lookup_listener(__tmp0._proxy_listener)

    def _lookup_removed(__tmp0, lookup: Lookup) -> None:
        result = __tmp0._results[lookup]

        if __tmp0._listeners:
            result.remove_lookup_listener(__tmp0._proxy_listener)

            # If this result contained some instances, trigger the listeners.
            # Use all_classes() (that should internally use Item.get_type()) instead of
            # all_instances() to avoid loading instances of converted items.
            if result.all_classes():
                __tmp0._proxy_listener(result)

        del __tmp0._results[lookup]
        del result

    def add_lookup_listener(__tmp0, listener: Callable[[Result], None]) -> None:
        if not __tmp0._listeners:
            for result in __tmp0._results.values():
                result.add_lookup_listener(__tmp0._proxy_listener)

        __tmp0._listeners.append(WeakCallable(listener, __tmp0._listeners.remove))

    def remove_lookup_listener(__tmp0, listener) -> None:
        __tmp0._listeners.remove(listener)  # type: ignore

        if not __tmp0._listeners:
            for result in __tmp0._results.values():
                result.remove_lookup_listener(__tmp0._proxy_listener)

    def _proxy_listener(__tmp0, result) :
        for listener in __tmp0._listeners:
            listener(__tmp0)

    def all_classes(__tmp0) -> AbstractSet[Type[object]]:
        return frozenset(chain(*(
            result.all_classes()
            for result in __tmp0._results.values()
        )))

    def all_instances(__tmp0) :
        return tuple(chain(*(
            result.all_instances()
            for result in __tmp0._results.values()
        )))

    def all_items(__tmp0) -> Sequence[Item]:
        return tuple(chain(*(
            result.all_items()
            for result in __tmp0._results.values()
        )))
