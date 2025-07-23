from typing import TypeAlias
__typ2 : TypeAlias = "Lookup"
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


class __typ1(__typ2):
    '''
    Implementation of a lookup that concile results from multiple lookups at the same time.
    '''

    def __init__(__tmp1, *lookups) :
        '''
        Creates a new ProxyLookup from an optional list of lookups to use as sources.

        :param lookups: Initial lookup sources.
        '''
        __tmp1._lookups = list(lookups)
        __tmp1._results: WeakValueDictionary[Type[object], __typ0] = WeakValueDictionary()

        super().__init__()

    def __tmp3(__tmp1, lookup) -> None:
        '''
        Adds a lookup to the list of sources for the proxy.
        Will update all results accordingly
        '''
        __tmp1._lookups.append(lookup)
        for result in __tmp1._results.values():
            result._lookup_added(lookup)

    def remove_lookup(__tmp1, lookup: __typ2) :
        '''
        Removes a lookup from the list of sources for the proxy.
        Will update all results accordingly
        '''
        __tmp1._lookups.remove(lookup)
        for result in __tmp1._results.values():
            result._lookup_removed(lookup)

    def lookup(__tmp1, __tmp2) :
        for lookup in __tmp1._lookups:
            obj = lookup(__tmp2)
            if obj is not None:
                return obj
        else:
            return None

    def lookup_item(__tmp1, __tmp2) :
        for lookup in __tmp1._lookups:
            item = lookup.lookup_item(__tmp2)
            if item is not None:
                return item
        else:
            return None

    def lookup_result(__tmp1, __tmp2) :
        result = __tmp1._results.get(__tmp2, None)
        if result is not None:
            return result

        result = __typ0(__tmp1, __tmp2)
        __tmp1._results[__tmp2] = result

        return result


class __typ0(Result):
    '''
    Implementation of a composite result that supports having multiple lookup sources.
    When _lookup_added() or _lookup_removed() are invoked (from ProxyLookup.add/remove_lookup()),
    listeners will be notified if instances appears or dissapears from the composite result.
    '''

    def __init__(__tmp1, lookup: __typ1, __tmp2) :
        __tmp1._lookup = lookup
        __tmp1._cls = __tmp2
        __tmp1._listeners: MutableSequence[WeakCallable] = []

        __tmp1._results = {
            lookup: lookup.lookup_result(__tmp2)
            for lookup in __tmp1._lookup._lookups
        }

    def _lookup_added(__tmp1, lookup: __typ2) :
        result = lookup.lookup_result(__tmp1._cls)
        __tmp1._results[lookup] = result

        if __tmp1._listeners:
            # If this new result already contains some instances, trigger the listeners.
            # Use all_classes() (that should internally use Item.get_type()) instead of
            # all_instances() to avoid loading instances of converted items.
            if result.all_classes():
                __tmp1._proxy_listener(result)

            result.add_lookup_listener(__tmp1._proxy_listener)

    def _lookup_removed(__tmp1, lookup) :
        result = __tmp1._results[lookup]

        if __tmp1._listeners:
            result.remove_lookup_listener(__tmp1._proxy_listener)

            # If this result contained some instances, trigger the listeners.
            # Use all_classes() (that should internally use Item.get_type()) instead of
            # all_instances() to avoid loading instances of converted items.
            if result.all_classes():
                __tmp1._proxy_listener(result)

        del __tmp1._results[lookup]
        del result

    def add_lookup_listener(__tmp1, __tmp0) :
        if not __tmp1._listeners:
            for result in __tmp1._results.values():
                result.add_lookup_listener(__tmp1._proxy_listener)

        __tmp1._listeners.append(WeakCallable(__tmp0, __tmp1._listeners.remove))

    def remove_lookup_listener(__tmp1, __tmp0: Callable[[Result], None]) :
        __tmp1._listeners.remove(__tmp0)  # type: ignore

        if not __tmp1._listeners:
            for result in __tmp1._results.values():
                result.remove_lookup_listener(__tmp1._proxy_listener)

    def _proxy_listener(__tmp1, result: <FILL>) :
        for __tmp0 in __tmp1._listeners:
            __tmp0(__tmp1)

    def all_classes(__tmp1) :
        return frozenset(chain(*(
            result.all_classes()
            for result in __tmp1._results.values()
        )))

    def all_instances(__tmp1) -> Sequence[object]:
        return tuple(chain(*(
            result.all_instances()
            for result in __tmp1._results.values()
        )))

    def all_items(__tmp1) :
        return tuple(chain(*(
            result.all_items()
            for result in __tmp1._results.values()
        )))
