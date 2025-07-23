from typing import TypeAlias
__typ1 : TypeAlias = "int"
__typ6 : TypeAlias = "bool"
__typ7 : TypeAlias = "ContextDict"
__typ4 : TypeAlias = "Component"
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


def __tmp4(iterable, key=None):
    return map(next, map(operator.itemgetter(1), itertools.groupby(iterable, key)))


class __typ2(AttributeConverter):
    @property
    def filter_ics_names(__tmp1) :
        return ["RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]

    def __tmp2(
        __tmp1, component, item, __tmp0
    ) :
        assert isinstance(item, ContentLine)
        key = (__tmp1, "lines")
        lines = __tmp0[key]
        if lines is None:
            lines = __tmp0[key] = []
        lines.append(item)
        return True

    def post_populate(__tmp1, component, __tmp0):
        lines_str = "".join(
            line.serialize(newline=True) for line in __tmp0.pop((__tmp1, "lines"))
        )
        # TODO only feed dateutil the params it likes, add the rest as extra
        tzinfos = __tmp0.get(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        rrule = dateutil.rrule.rrulestr(lines_str, tzinfos=tzinfos, compatible=True)
        rrule._rdate = list(__tmp4(sorted(rrule._rdate)))  # type: ignore
        rrule._exdate = list(__tmp4(sorted(rrule._exdate)))  # type: ignore
        __tmp1.set_or_append_value(component, rrule)

    def serialize(__tmp1, component, output, __tmp0):
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
                output.append(ContentLine(name="DTSTART", value=dt_value))

        for rrule in value._rrule:
            output.append(rrule_to_ContentLine(rrule))
        for exrule in value._exrule:
            cl = rrule_to_ContentLine(exrule)
            cl.name = "EXRULE"
            output.append(cl)
        for rdate in __tmp4(sorted(value._rdate)):
            output.append(
                ContentLine(name="RDATE", value=DatetimeConverter.serialize(rdate))
            )
        for exdate in __tmp4(sorted(value._exdate)):
            output.append(
                ContentLine(name="EXDATE", value=DatetimeConverter.serialize(exdate))
            )

    def post_serialize(
        __tmp1, component, output: <FILL>, __tmp0
    ):
        __tmp0.pop("DTSTART", None)


AttributeConverter.BY_TYPE[dateutil.rrule.rruleset] = __typ2


class __typ0(GenericConverter):
    CONTEXT_FIELD = "ALARM_ACTION"

    @property
    def __tmp3(__tmp1) :
        return 1000

    @property
    def filter_ics_names(__tmp1) :
        return ["ACTION"]

    def __tmp2(
        __tmp1, component, item, __tmp0
    ) :
        assert isinstance(item, ContentLine)
        assert issubclass(type(component), get_type_from_action(item.value))
        if item.params:
            component.extra_params["ACTION"] = copy_extra_params(item.params)
        return True

    def serialize(__tmp1, component, output, __tmp0):
        assert isinstance(component, BaseAlarm)
        output.append(
            ContentLine(
                name="ACTION",
                params=cast(ExtraParams, component.extra_params.get("ACTION", {})),
                value=component.action,
            )
        )


class __typ3(ComponentMeta):
    def find_converters(__tmp1) :
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

    def load_instance(
        __tmp1, container, __tmp0: Optional[__typ7] = None
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


ComponentMeta.BY_TYPE[BaseAlarm] = __typ3(BaseAlarm)
ComponentMeta.BY_TYPE[AudioAlarm] = __typ3(AudioAlarm)
ComponentMeta.BY_TYPE[CustomAlarm] = __typ3(CustomAlarm)
ComponentMeta.BY_TYPE[DisplayAlarm] = __typ3(DisplayAlarm)
ComponentMeta.BY_TYPE[EmailAlarm] = __typ3(EmailAlarm)
ComponentMeta.BY_TYPE[NoneAlarm] = __typ3(NoneAlarm)
