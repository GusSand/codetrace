from typing import TypeAlias
__typ3 : TypeAlias = "Component"
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "bool"
__typ4 : TypeAlias = "ContainerItem"
__typ6 : TypeAlias = "ContextDict"
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

    def find_converters(self):
        return sort_converters(
            itertools.chain(super().find_converters(), (__typ2(),))
        )

    def _populate_attrs(
        self, instance: __typ3, container, context
    ):
        assert isinstance(instance, Calendar)
        avail_tz: Dict[str, Timezone] = context.setdefault(
            DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
        )
        for child in container:
            if child.name == Timezone.NAME and isinstance(child, Container):
                tz = Timezone.from_container(child)
                avail_tz.setdefault(tz.tzid, tz)

        super()._populate_attrs(instance, container, context)

    def _serialize_attrs(
        self, component, context, container: <FILL>
    ):
        assert isinstance(component, Calendar)
        context.setdefault(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        super()._serialize_attrs(component, context, container)

        # serialize all used timezones
        timezones = [
            tz.to_container()
            for tz in context[DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ].values()
        ]
        # insert them at the place where they usually would have been serialized
        split = context["VTIMEZONES_AFTER"]
        container.data = container.data[:split] + timezones + container.data[split:]


class __typ2(GenericConverter):
    @property
    def priority(self) :
        return 600

    @property
    def filter_ics_names(self) -> List[str]:
        return [Timezone.NAME]

    def populate(
        self, component, item: __typ4, context
    ) -> __typ5:
        # don't actually load anything, as that has already been done before all other deserialization in `CalendarMeta`
        return item.name == Timezone.NAME and isinstance(item, Container)

    def serialize(self, component: __typ3, output: Container, context):
        # store the place where we should insert all the timezones
        context["VTIMEZONES_AFTER"] = len(output)


ComponentMeta.BY_TYPE[Calendar] = __typ1(Calendar)
