from typing import TypeAlias
__typ0 : TypeAlias = "ContextDict"
__typ2 : TypeAlias = "ContainerItem"
__typ3 : TypeAlias = "Container"
__typ1 : TypeAlias = "Component"
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


class TimezoneMeta(ImmutableComponentMeta):
    def load_instance(
        __tmp2, __tmp1, __tmp3: Optional[__typ0] = None
    ):
        # TODO  The mandatory "DTSTART" property gives the effective onset date
        #       and local time for the time zone sub-component definition.
        #       "DTSTART" in this usage MUST be specified as a date with a local
        #       time value.

        instance = super().load_instance(__tmp1, __tmp3)
        if __tmp3 is not None:
            available_tz = __tmp3.setdefault(
                DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
            )
            available_tz.setdefault(instance.tzid, instance)
        return instance


class TimezoneObservanceMemberMeta(AttributeConverter):
    @property
    def filter_ics_names(__tmp2) :
        return [TimezoneStandardObservance.NAME, TimezoneDaylightObservance.NAME]

    def __tmp5(
        __tmp2, component, item: __typ2, __tmp3
    ) :
        assert isinstance(item, __typ3)
        if item.name.upper() == TimezoneStandardObservance.NAME:
            __tmp2.set_or_append_value(
                component, TimezoneStandardObservance.from_container(item, __tmp3)
            )
        elif item.name.upper() == TimezoneDaylightObservance.NAME:
            __tmp2.set_or_append_value(
                component, TimezoneDaylightObservance.from_container(item, __tmp3)
            )
        else:
            raise ValueError(
                "can't populate TimezoneObservance from {} {}: {}".format(
                    type(item), item.name, item
                )
            )
        return True

    def serialize(__tmp2, __tmp0, __tmp4: __typ3, __tmp3):
        extras = __tmp2.get_extra_params(__tmp0)
        if extras:
            raise ValueError(
                "ComponentConverter %s can't serialize extra params %s", (__tmp2, extras)
            )
        for value in __tmp2.get_value_list(__tmp0):
            __tmp4.append(value.to_container(__tmp3))


class TimezoneObservanceMeta(ImmutableComponentMeta):
    def __tmp6(__tmp2, attribute: <FILL>):
        return TimezoneObservanceMemberMeta(attribute)


ComponentMeta.BY_TYPE[TimezoneObservance] = TimezoneObservanceMeta(TimezoneObservance)
ComponentMeta.BY_TYPE[TimezoneStandardObservance] = ImmutableComponentMeta(
    TimezoneStandardObservance
)
ComponentMeta.BY_TYPE[TimezoneDaylightObservance] = ImmutableComponentMeta(
    TimezoneDaylightObservance
)
ComponentMeta.BY_TYPE[Timezone] = TimezoneMeta(Timezone)
