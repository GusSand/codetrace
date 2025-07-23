from typing import TypeAlias
__typ3 : TypeAlias = "ContainerItem"
__typ4 : TypeAlias = "Attribute"
__typ2 : TypeAlias = "ContextDict"
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
        __tmp2, __tmp1, __tmp3: Optional[__typ2] = None
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


class __typ0(AttributeConverter):
    @property
    def __tmp5(__tmp2) :
        return [TimezoneStandardObservance.NAME, TimezoneDaylightObservance.NAME]

    def __tmp8(
        __tmp2, component, __tmp6, __tmp3: __typ2
    ) :
        assert isinstance(__tmp6, Container)
        if __tmp6.name.upper() == TimezoneStandardObservance.NAME:
            __tmp2.set_or_append_value(
                component, TimezoneStandardObservance.from_container(__tmp6, __tmp3)
            )
        elif __tmp6.name.upper() == TimezoneDaylightObservance.NAME:
            __tmp2.set_or_append_value(
                component, TimezoneDaylightObservance.from_container(__tmp6, __tmp3)
            )
        else:
            raise ValueError(
                "can't populate TimezoneObservance from {} {}: {}".format(
                    type(__tmp6), __tmp6.name, __tmp6
                )
            )
        return True

    def __tmp10(__tmp2, __tmp0: Component, __tmp4: <FILL>, __tmp3):
        extras = __tmp2.get_extra_params(__tmp0)
        if extras:
            raise ValueError(
                "ComponentConverter %s can't serialize extra params %s", (__tmp2, extras)
            )
        for value in __tmp2.get_value_list(__tmp0):
            __tmp4.append(value.to_container(__tmp3))


class TimezoneObservanceMeta(ImmutableComponentMeta):
    def __tmp9(__tmp2, __tmp7):
        return __typ0(__tmp7)


ComponentMeta.BY_TYPE[TimezoneObservance] = TimezoneObservanceMeta(TimezoneObservance)
ComponentMeta.BY_TYPE[TimezoneStandardObservance] = ImmutableComponentMeta(
    TimezoneStandardObservance
)
ComponentMeta.BY_TYPE[TimezoneDaylightObservance] = ImmutableComponentMeta(
    TimezoneDaylightObservance
)
ComponentMeta.BY_TYPE[Timezone] = __typ1(Timezone)
