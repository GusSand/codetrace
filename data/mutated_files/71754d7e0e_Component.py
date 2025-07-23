from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "ContextDict"
__typ4 : TypeAlias = "bool"
__typ3 : TypeAlias = "Container"
__typ5 : TypeAlias = "ContainerItem"
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
            itertools.chain(super().find_converters(), (__typ2(),))
        )

    def _populate_attrs(
        __tmp1, instance: Component, __tmp0, context: __typ1
    ):
        assert isinstance(instance, Calendar)
        avail_tz: Dict[str, Timezone] = context.setdefault(
            DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
        )
        for child in __tmp0:
            if child.name == Timezone.NAME and isinstance(child, __typ3):
                tz = Timezone.from_container(child)
                avail_tz.setdefault(tz.tzid, tz)

        super()._populate_attrs(instance, __tmp0, context)

    def _serialize_attrs(
        __tmp1, component, context: __typ1, __tmp0: __typ3
    ):
        assert isinstance(component, Calendar)
        context.setdefault(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        super()._serialize_attrs(component, context, __tmp0)

        # serialize all used timezones
        timezones = [
            tz.to_container()
            for tz in context[DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ].values()
        ]
        # insert them at the place where they usually would have been serialized
        split = context["VTIMEZONES_AFTER"]
        __tmp0.data = __tmp0.data[:split] + timezones + __tmp0.data[split:]


class __typ2(GenericConverter):
    @property
    def priority(__tmp1) -> __typ0:
        return 600

    @property
    def filter_ics_names(__tmp1) :
        return [Timezone.NAME]

    def populate(
        __tmp1, component, item, context
    ) -> __typ4:
        # don't actually load anything, as that has already been done before all other deserialization in `CalendarMeta`
        return item.name == Timezone.NAME and isinstance(item, __typ3)

    def __tmp2(__tmp1, component: <FILL>, output: __typ3, context: __typ1):
        # store the place where we should insert all the timezones
        context["VTIMEZONES_AFTER"] = len(output)


ComponentMeta.BY_TYPE[Calendar] = CalendarMeta(Calendar)
