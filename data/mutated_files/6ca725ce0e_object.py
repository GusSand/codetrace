from typing import TypeAlias
__typ4 : TypeAlias = "Result"
__typ3 : TypeAlias = "Item"
__typ1 : TypeAlias = "str"
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


class __typ2(Lookup):
    '''
    Unmodifiable lookup that contains just one fixed object.
    '''

    def __tmp7(__tmp0, __tmp4: <FILL>, id_: __typ1 = None) :
        '''
        :param member: The only fixed instance in this lookup.
        :param id_: Persistent identifier for member.
        '''
        if __tmp4 is None:
            raise ValueError('None cannot be a lookup member')

        __tmp0._member = __tmp4
        __tmp0._id = id_

    def lookup(__tmp0, __tmp6: Type[object]) -> Optional[object]:
        if isinstance(__tmp0._member, __tmp6):
            return __tmp0._member
        else:
            return None

    def lookup_result(__tmp0, __tmp6: Type[object]) :
        __tmp2 = __tmp0.lookup_item(__tmp6)
        if __tmp2 is not None:
            return __typ0(__tmp2)
        else:
            return lookups.EmptyLookup().lookup_result(__tmp6)

    def lookup_item(__tmp0, __tmp6) :
        if isinstance(__tmp0._member, __tmp6):
            return lookups.LookupItem(__tmp0._member, __tmp0._id)
        else:
            return None

    def __tmp3(__tmp0, __tmp6: Type[object]) -> Sequence[object]:
        if isinstance(__tmp0._member, __tmp6):
            return (__tmp0._member, )
        else:
            return tuple()

    def __tmp9(__tmp0) -> __typ1:
        return 'SingletonLookup[%s]' % __typ1(__tmp0._member)


class __typ0(__typ4):

    def __tmp7(__tmp0, __tmp2) -> None:
        __tmp0._item = __tmp2

    def add_lookup_listener(__tmp0, __tmp5) -> None:
        pass

    def remove_lookup_listener(__tmp0, __tmp5: Callable[[__typ4], None]) :
        pass

    def __tmp1(__tmp0) -> AbstractSet[Type[object]]:
        return frozenset((__tmp0._item.get_type(), ))

    def all_instances(__tmp0) :
        instance = __tmp0._item.get_instance()
        if instance is not None:
            return __tmp0._item.get_instance(),
        else:
            return tuple()

    def __tmp8(__tmp0) :
        return __tmp0._item,
