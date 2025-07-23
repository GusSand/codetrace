from typing import TypeAlias
__typ4 : TypeAlias = "ContainerItem"
__typ5 : TypeAlias = "ContextDict"
__typ3 : TypeAlias = "Component"
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


class __typ1(ComponentMeta):
    """
    Slightly modified meta class for Calendars that makes sure that `Timezone`s are always loaded first
      and that all contained timezones are serialized.
    """

    def find_converters(__tmp1):
        return sort_converters(
            itertools.chain(super().find_converters(), (__typ2(),))
        )

    def _populate_attrs(
        __tmp1, __tmp3, container, __tmp0
    ):
        assert isinstance(__tmp3, Calendar)
        avail_tz: Dict[str, Timezone] = __tmp0.setdefault(
            DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
        )
        for child in container:
            if child.name == Timezone.NAME and isinstance(child, Container):
                tz = Timezone.from_container(child)
                avail_tz.setdefault(tz.tzid, tz)

        super()._populate_attrs(__tmp3, container, __tmp0)

    def _serialize_attrs(
        __tmp1, component: __typ3, __tmp0: __typ5, container: Container
    ):
        assert isinstance(component, Calendar)
        __tmp0.setdefault(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        super()._serialize_attrs(component, __tmp0, container)

        # serialize all used timezones
        timezones = [
            tz.to_container()
            for tz in __tmp0[DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ].values()
        ]
        # insert them at the place where they usually would have been serialized
        split = __tmp0["VTIMEZONES_AFTER"]
        container.data = container.data[:split] + timezones + container.data[split:]


class __typ2(GenericConverter):
    @property
    def priority(__tmp1) :
        return 600

    @property
    def filter_ics_names(__tmp1) :
        return [Timezone.NAME]

    def __tmp4(
        __tmp1, component, __tmp2: __typ4, __tmp0
    ) -> bool:
        # don't actually load anything, as that has already been done before all other deserialization in `CalendarMeta`
        return __tmp2.name == Timezone.NAME and isinstance(__tmp2, Container)

    def serialize(__tmp1, component: __typ3, output: <FILL>, __tmp0):
        # store the place where we should insert all the timezones
        __tmp0["VTIMEZONES_AFTER"] = len(output)


ComponentMeta.BY_TYPE[Calendar] = __typ1(Calendar)
