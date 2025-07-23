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


class __typ0(Lookup):
    '''
    Unmodifiable lookup that contains just one fixed object.
    '''

    def __tmp5(__tmp0, __tmp2, id_: str = None) :
        '''
        :param member: The only fixed instance in this lookup.
        :param id_: Persistent identifier for member.
        '''
        if __tmp2 is None:
            raise ValueError('None cannot be a lookup member')

        __tmp0._member = __tmp2
        __tmp0._id = id_

    def lookup(__tmp0, __tmp4) :
        if isinstance(__tmp0._member, __tmp4):
            return __tmp0._member
        else:
            return None

    def lookup_result(__tmp0, __tmp4) :
        item = __tmp0.lookup_item(__tmp4)
        if item is not None:
            return SingletonResult(item)
        else:
            return lookups.EmptyLookup().lookup_result(__tmp4)

    def lookup_item(__tmp0, __tmp4) -> Optional[Item]:
        if isinstance(__tmp0._member, __tmp4):
            return lookups.LookupItem(__tmp0._member, __tmp0._id)
        else:
            return None

    def __tmp1(__tmp0, __tmp4) :
        if isinstance(__tmp0._member, __tmp4):
            return (__tmp0._member, )
        else:
            return tuple()

    def __str__(__tmp0) :
        return 'SingletonLookup[%s]' % str(__tmp0._member)


class SingletonResult(Result):

    def __tmp5(__tmp0, item: <FILL>) -> None:
        __tmp0._item = item

    def add_lookup_listener(__tmp0, listener) :
        pass

    def remove_lookup_listener(__tmp0, listener) :
        pass

    def all_classes(__tmp0) :
        return frozenset((__tmp0._item.get_type(), ))

    def __tmp3(__tmp0) :
        instance = __tmp0._item.get_instance()
        if instance is not None:
            return __tmp0._item.get_instance(),
        else:
            return tuple()

    def __tmp6(__tmp0) :
        return __tmp0._item,
