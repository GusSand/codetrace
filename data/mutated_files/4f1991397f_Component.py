from typing import TypeAlias
__typ5 : TypeAlias = "ContainerItem"
__typ4 : TypeAlias = "bool"
__typ2 : TypeAlias = "Container"
__typ6 : TypeAlias = "ContextDict"
from typing import List, Optional

from attr import Attribute

from ics.component import Component
from ics.contentline import Container
from ics.converter.base import AttributeConverter
from ics.converter.component import ComponentMeta, ImmutableComponentMeta
from ics.timezone import (
    Timezone,
    TimezoneDaylightObservance,
    TimezoneObservance,
    TimezoneStandardObservance,
)
from ics.types import ContainerItem, ContextDict
from ics.valuetype.datetime import DatetimeConverterMixin


class __typ1(ImmutableComponentMeta):
    def load_instance(
        __tmp2, container: __typ2, __tmp0: Optional[__typ6] = None
    ):
        # TODO  The mandatory "DTSTART" property gives the effective onset date
        #       and local time for the time zone sub-component definition.
        #       "DTSTART" in this usage MUST be specified as a date with a local
        #       time value.

        instance = super().load_instance(container, __tmp0)
        if __tmp0 is not None:
            available_tz = __tmp0.setdefault(
                DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
            )
            available_tz.setdefault(instance.tzid, instance)
        return instance


class __typ0(AttributeConverter):
    @property
    def filter_ics_names(__tmp2) :
        return [TimezoneStandardObservance.NAME, TimezoneDaylightObservance.NAME]

    def __tmp3(
        __tmp2, component, item: __typ5, __tmp0
    ) :
        assert isinstance(item, __typ2)
        if item.name.upper() == TimezoneStandardObservance.NAME:
            __tmp2.set_or_append_value(
                component, TimezoneStandardObservance.from_container(item, __tmp0)
            )
        elif item.name.upper() == TimezoneDaylightObservance.NAME:
            __tmp2.set_or_append_value(
                component, TimezoneDaylightObservance.from_container(item, __tmp0)
            )
        else:
            raise ValueError(
                "can't populate TimezoneObservance from {} {}: {}".format(
                    type(item), item.name, item
                )
            )
        return True

    def serialize(__tmp2, parent: <FILL>, output: __typ2, __tmp0: __typ6):
        extras = __tmp2.get_extra_params(parent)
        if extras:
            raise ValueError(
                "ComponentConverter %s can't serialize extra params %s", (__tmp2, extras)
            )
        for value in __tmp2.get_value_list(parent):
            output.append(value.to_container(__tmp0))


class __typ3(ImmutableComponentMeta):
    def __call__(__tmp2, __tmp1: Attribute):
        return __typ0(__tmp1)


ComponentMeta.BY_TYPE[TimezoneObservance] = __typ3(TimezoneObservance)
ComponentMeta.BY_TYPE[TimezoneStandardObservance] = ImmutableComponentMeta(
    TimezoneStandardObservance
)
ComponentMeta.BY_TYPE[TimezoneDaylightObservance] = ImmutableComponentMeta(
    TimezoneDaylightObservance
)
ComponentMeta.BY_TYPE[Timezone] = __typ1(Timezone)
