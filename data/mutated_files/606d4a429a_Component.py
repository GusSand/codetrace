from typing import TypeAlias
__typ1 : TypeAlias = "Attribute"
__typ4 : TypeAlias = "ContextDict"
__typ2 : TypeAlias = "Container"
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


class __typ0(ImmutableComponentMeta):
    def load_instance(
        __tmp1, __tmp0, context: Optional[__typ4] = None
    ):
        # TODO  The mandatory "DTSTART" property gives the effective onset date
        #       and local time for the time zone sub-component definition.
        #       "DTSTART" in this usage MUST be specified as a date with a local
        #       time value.

        instance = super().load_instance(__tmp0, context)
        if context is not None:
            available_tz = context.setdefault(
                DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {}
            )
            available_tz.setdefault(instance.tzid, instance)
        return instance


class TimezoneObservanceMemberMeta(AttributeConverter):
    @property
    def __tmp8(__tmp1) :
        return [TimezoneStandardObservance.NAME, TimezoneDaylightObservance.NAME]

    def __tmp6(
        __tmp1, component: <FILL>, __tmp3, context: __typ4
    ) :
        assert isinstance(__tmp3, __typ2)
        if __tmp3.name.upper() == TimezoneStandardObservance.NAME:
            __tmp1.set_or_append_value(
                component, TimezoneStandardObservance.from_container(__tmp3, context)
            )
        elif __tmp3.name.upper() == TimezoneDaylightObservance.NAME:
            __tmp1.set_or_append_value(
                component, TimezoneDaylightObservance.from_container(__tmp3, context)
            )
        else:
            raise ValueError(
                "can't populate TimezoneObservance from {} {}: {}".format(
                    type(__tmp3), __tmp3.name, __tmp3
                )
            )
        return True

    def __tmp4(__tmp1, parent, __tmp2: __typ2, context: __typ4):
        extras = __tmp1.get_extra_params(parent)
        if extras:
            raise ValueError(
                "ComponentConverter %s can't serialize extra params %s", (__tmp1, extras)
            )
        for value in __tmp1.get_value_list(parent):
            __tmp2.append(value.to_container(context))


class __typ3(ImmutableComponentMeta):
    def __tmp7(__tmp1, __tmp5: __typ1):
        return TimezoneObservanceMemberMeta(__tmp5)


ComponentMeta.BY_TYPE[TimezoneObservance] = __typ3(TimezoneObservance)
ComponentMeta.BY_TYPE[TimezoneStandardObservance] = ImmutableComponentMeta(
    TimezoneStandardObservance
)
ComponentMeta.BY_TYPE[TimezoneDaylightObservance] = ImmutableComponentMeta(
    TimezoneDaylightObservance
)
ComponentMeta.BY_TYPE[Timezone] = __typ0(Timezone)
