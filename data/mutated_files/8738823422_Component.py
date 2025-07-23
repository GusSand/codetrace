from typing import TypeAlias
__typ1 : TypeAlias = "int"
__typ4 : TypeAlias = "bool"
__typ3 : TypeAlias = "Container"
__typ2 : TypeAlias = "ContextDict"
__typ5 : TypeAlias = "ContainerItem"
import itertools
import operator
from typing import TYPE_CHECKING, Iterable, List, Optional, cast

import attr
import dateutil.rrule

from ics import (
    AudioAlarm,
    BaseAlarm,
    CustomAlarm,
    DisplayAlarm,
    EmailAlarm,
    NoneAlarm,
    get_type_from_action,
)
from ics.component import Component
from ics.contentline import Container, ContentLine
from ics.converter.base import AttributeConverter, GenericConverter, sort_converters
from ics.converter.component import ComponentMeta
from ics.rrule import rrule_to_ContentLine
from ics.types import ContainerItem, ContextDict, ExtraParams, copy_extra_params
from ics.utils import one
from ics.valuetype.datetime import DatetimeConverter, DatetimeConverterMixin


def __tmp12(__tmp9, key=None):
    return map(next, map(operator.itemgetter(1), itertools.groupby(__tmp9, key)))


class RecurrenceConverter(AttributeConverter):
    @property
    def __tmp10(__tmp1) :
        return ["RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]

    def __tmp5(
        __tmp1, component, __tmp4, __tmp0
    ) :
        assert isinstance(__tmp4, ContentLine)
        key = (__tmp1, "lines")
        lines = __tmp0[key]
        if lines is None:
            lines = __tmp0[key] = []
        lines.append(__tmp4)
        return True

    def __tmp2(__tmp1, component, __tmp0):
        lines_str = "".join(
            line.serialize(newline=True) for line in __tmp0.pop((__tmp1, "lines"))
        )
        # TODO only feed dateutil the params it likes, add the rest as extra
        tzinfos = __tmp0.get(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        rrule = dateutil.rrule.rrulestr(lines_str, tzinfos=tzinfos, compatible=True)
        rrule._rdate = list(__tmp12(sorted(rrule._rdate)))  # type: ignore
        rrule._exdate = list(__tmp12(sorted(rrule._exdate)))  # type: ignore
        __tmp1.set_or_append_value(component, rrule)

    def serialize(__tmp1, component, __tmp3, __tmp0):
        value = __tmp1.get_value(component)
        if not TYPE_CHECKING:
            assert isinstance(value, dateutil.rrule.rruleset)
        for rrule in itertools.chain(value._rrule, value._exrule):
            if rrule._dtstart is None:
                continue
            # check that the rrule uses the same DTSTART as a possible Timespan(Converter)
            dtstart = __tmp0["DTSTART"]
            if dtstart:
                if dtstart != rrule._dtstart:
                    raise ValueError("differing DTSTART values")
            else:
                __tmp0["DTSTART"] = rrule._dtstart
                dt_value = DatetimeConverter.serialize(rrule._dtstart, __tmp0=__tmp0)
                __tmp3.append(ContentLine(name="DTSTART", value=dt_value))

        for rrule in value._rrule:
            __tmp3.append(rrule_to_ContentLine(rrule))
        for exrule in value._exrule:
            cl = rrule_to_ContentLine(exrule)
            cl.name = "EXRULE"
            __tmp3.append(cl)
        for rdate in __tmp12(sorted(value._rdate)):
            __tmp3.append(
                ContentLine(name="RDATE", value=DatetimeConverter.serialize(rdate))
            )
        for exdate in __tmp12(sorted(value._exdate)):
            __tmp3.append(
                ContentLine(name="EXDATE", value=DatetimeConverter.serialize(exdate))
            )

    def __tmp11(
        __tmp1, component: <FILL>, __tmp3: __typ3, __tmp0
    ):
        __tmp0.pop("DTSTART", None)


AttributeConverter.BY_TYPE[dateutil.rrule.rruleset] = RecurrenceConverter


class __typ0(GenericConverter):
    CONTEXT_FIELD = "ALARM_ACTION"

    @property
    def __tmp6(__tmp1) :
        return 1000

    @property
    def __tmp10(__tmp1) :
        return ["ACTION"]

    def __tmp5(
        __tmp1, component, __tmp4, __tmp0
    ) :
        assert isinstance(__tmp4, ContentLine)
        assert issubclass(type(component), get_type_from_action(__tmp4.value))
        if __tmp4.params:
            component.extra_params["ACTION"] = copy_extra_params(__tmp4.params)
        return True

    def serialize(__tmp1, component, __tmp3, __tmp0):
        assert isinstance(component, BaseAlarm)
        __tmp3.append(
            ContentLine(
                name="ACTION",
                params=cast(ExtraParams, component.extra_params.get("ACTION", {})),
                value=component.action,
            )
        )


class AlarmMeta(ComponentMeta):
    def __tmp7(__tmp1) :
        convs: List[GenericConverter] = [
            c
            for c in (
                AttributeConverter.get_converter_for(a)
                for a in attr.fields(__tmp1.component_type)
            )
            if c is not None
        ]
        convs.append(__typ0())
        return sort_converters(convs)

    def __tmp8(
        __tmp1, container, __tmp0: Optional[__typ2] = None
    ):
        clazz = get_type_from_action(
            one(
                container["ACTION"],
                too_short="VALARM must have exactly one ACTION!",
                too_long="VALARM must have exactly one ACTION, but got {first!r}, {second!r}, and possibly more!",
            ).value
        )
        instance = clazz()
        ComponentMeta.BY_TYPE[clazz].populate_instance(instance, container, __tmp0)
        return instance


ComponentMeta.BY_TYPE[BaseAlarm] = AlarmMeta(BaseAlarm)
ComponentMeta.BY_TYPE[AudioAlarm] = AlarmMeta(AudioAlarm)
ComponentMeta.BY_TYPE[CustomAlarm] = AlarmMeta(CustomAlarm)
ComponentMeta.BY_TYPE[DisplayAlarm] = AlarmMeta(DisplayAlarm)
ComponentMeta.BY_TYPE[EmailAlarm] = AlarmMeta(EmailAlarm)
ComponentMeta.BY_TYPE[NoneAlarm] = AlarmMeta(NoneAlarm)
