from typing import TypeAlias
__typ0 : TypeAlias = "LookupProvider"
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Contributors as noted in the AUTHORS file
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Provides a lookup that redirects to another (dynamic) lookup, through a LookupProvider.
'''
# In original Java lookups, it corresponds to SimpleProxyLookup,
# itself accessible through Lookups.proxy().

# System imports
from typing import Sequence, MutableSequence, AbstractSet, Type, Optional, Callable
from weakref import WeakValueDictionary

# Third-party imports

# Local imports
from .lookup import Lookup, Item, Result, LookupProvider
from .weak_observable import WeakCallable


class DelegatedLookup(Lookup):
    '''
    Implementation of a lookup that forward all requests to another lookup. The point being that
    the other lookup can change completely (ie. be a different object instance). This lookup remains
    the same object (obviously) and take care of handing over all the outstanding results and
    listener subscriptions to the new lookup.

    The delegate lookup is given by a LookupProvider. Just remember to call lookup_updated()
    whenever the delegate lookup changes.
    '''

    def __tmp1(__tmp0, provider) :
        '''
        Creates a new DelegatedLookup that gets its delegate from the supplied LookupProvider.
        The provider is immediately asked for a Lookup.

        :param provider: Lookup provider that will be asked when lookup_updated() is invoked.
        '''
        __tmp0._provider = provider
        __tmp0._delegate = provider.get_lookup()
        __tmp0._results: WeakValueDictionary[Type[object], DelegatedResult] = WeakValueDictionary()

    def lookup_updated(__tmp0) -> None:
        '''
        Check for change in delegate lookup. This method purposedly does not take any lookup in
        parameter. Because only the provider given at creation time can supply a new lookup. The
        lookup provider is a priviledged API.
        '''
        lookup = __tmp0._provider.get_lookup()
        if __tmp0._delegate != lookup:
            __tmp0._delegate = lookup

            for result in __tmp0._results.values():
                result.lookup_updated()

    @property
    def delegate(__tmp0) :
        '''Returns the lookup we currently delegate to.'''
        return __tmp0._delegate

    def lookup(__tmp0, cls) -> Optional[object]:
        return __tmp0._delegate.lookup(cls)

    def lookup_result(__tmp0, cls) :
        result = __tmp0._results.get(cls, None)
        if result is not None:
            return result

        result = DelegatedResult(__tmp0, cls)
        __tmp0._results[cls] = result

        return result


class DelegatedResult(Result):
    '''
    Implementation of a result that supports changing lookup source.
    When lookup_updated() is invoked (from DelegatedLookup.lookup_updated()), the actual result is
    switched over from the old lookup delegate to the new. Listeners are also notified if the
    switch over happens to modify the content of this result.
    '''

    def __tmp1(__tmp0, lookup, cls) :
        '''
        Creates a new DelegatedResult for the given class.

        A result is immediately asked to the delegate lookup.
        '''
        __tmp0._lookup = lookup
        __tmp0._cls = cls
        __tmp0._delegate = __tmp0._lookup.delegate.lookup_result(__tmp0._cls)
        __tmp0._listeners: MutableSequence[WeakCallable] = []

    def lookup_updated(__tmp0) :
        result = __tmp0._lookup.delegate.lookup_result(__tmp0._cls)
        if result != __tmp0._delegate:
            old_result, __tmp0._delegate = __tmp0._delegate, result

            if __tmp0._listeners:
                old_result.remove_lookup_listener(__tmp0._proxy_listener)

                # If these results contains some instances, trigger the listeners.
                # Use all_classes() (that should internally use Item.get_type()) instead of
                # all_instances() to avoid loading instances of converted items.
                if old_result.all_classes() or result.all_classes():
                    __tmp0._proxy_listener(result)

                result.add_lookup_listener(__tmp0._proxy_listener)

            del old_result  # Explicit

    def add_lookup_listener(__tmp0, listener) :
        if not __tmp0._listeners:
            __tmp0._delegate.add_lookup_listener(__tmp0._proxy_listener)

        __tmp0._listeners.append(WeakCallable(listener, __tmp0._listeners.remove))

    def remove_lookup_listener(__tmp0, listener) :
        __tmp0._listeners.remove(listener)  # type: ignore

        if not __tmp0._listeners:
            __tmp0._delegate.remove_lookup_listener(__tmp0._proxy_listener)

    def _proxy_listener(__tmp0, result: <FILL>) :
        for listener in __tmp0._listeners:
            listener(__tmp0)

    def all_classes(__tmp0) :
        return __tmp0._delegate.all_classes()

    def all_instances(__tmp0) :
        return __tmp0._delegate.all_instances()

    def all_items(__tmp0) :
        return __tmp0._delegate.all_items()
