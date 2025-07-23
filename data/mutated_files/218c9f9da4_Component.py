from typing import TypeAlias
__typ3 : TypeAlias = "ContainerItem"
__typ4 : TypeAlias = "ContextDict"
__typ2 : TypeAlias = "Container"
__typ0 : TypeAlias = "int"
import itertools
from typing import Dict, List

from ics import Calendar
from ics.component import Component
from ics.contentline import Container
from ics.converter.base import GenericConverter, sort_converters
from ics.converter.component import ComponentMeta
from ics.timezone import Timezone
from ics.types import ContainerItem, ContextDict
from ics.valuetype.datetime import DatetimeConverterMixin


class CalendarMeta(ComponentMeta):
    """
    Slightly modified meta class for Calendars that makes sure that `Timezone`s are always loaded first
      and that all contained timezones are serialized.
    """

    def find_converters(__tmp1):
        return sort_converters(
            itertools.chain(super().find_converters(), (__typ1(),))
        )

    def _populate_attrs(
        __tmp1, __tmp6: <FILL>, __tmp0, __tmp2
    ):
        assert isinstance(__tmp6, Calendar)
        avail_tz: Dict[str, Timezone] = __tmp2.setdefault(
            DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
        )
        for child in __tmp0:
            if child.name == Timezone.NAME and isinstance(child, __typ2):
                tz = Timezone.from_container(child)
                avail_tz.setdefault(tz.tzid, tz)

        super()._populate_attrs(__tmp6, __tmp0, __tmp2)

    def _serialize_attrs(
        __tmp1, component, __tmp2, __tmp0
    ):
        assert isinstance(component, Calendar)
        __tmp2.setdefault(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        super()._serialize_attrs(component, __tmp2, __tmp0)

        # serialize all used timezones
        timezones = [
            tz.to_container()
            for tz in __tmp2[DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ].values()
        ]
        # insert them at the place where they usually would have been serialized
        split = __tmp2["VTIMEZONES_AFTER"]
        __tmp0.data = __tmp0.data[:split] + timezones + __tmp0.data[split:]


class __typ1(GenericConverter):
    @property
    def __tmp8(__tmp1) :
        return 600

    @property
    def __tmp4(__tmp1) :
        return [Timezone.NAME]

    def __tmp7(
        __tmp1, component, __tmp5, __tmp2
    ) :
        # don't actually load anything, as that has already been done before all other deserialization in `CalendarMeta`
        return __tmp5.name == Timezone.NAME and isinstance(__tmp5, __typ2)

    def __tmp9(__tmp1, component, __tmp3, __tmp2):
        # store the place where we should insert all the timezones
        __tmp2["VTIMEZONES_AFTER"] = len(__tmp3)


ComponentMeta.BY_TYPE[Calendar] = CalendarMeta(Calendar)
