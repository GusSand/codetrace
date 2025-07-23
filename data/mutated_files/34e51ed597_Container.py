from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ4 : TypeAlias = "ContextDict"
__typ3 : TypeAlias = "Component"
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


def __tmp5(iterable, key=None):
    return map(next, map(operator.itemgetter(1), itertools.groupby(iterable, key)))


class __typ1(AttributeConverter):
    @property
    def __tmp3(__tmp0) :
        return ["RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]

    def __tmp2(
        __tmp0, component, item, context
    ) -> __typ2:
        assert isinstance(item, ContentLine)
        key = (__tmp0, "lines")
        lines = context[key]
        if lines is None:
            lines = context[key] = []
        lines.append(item)
        return True

    def post_populate(__tmp0, component: __typ3, context: __typ4):
        lines_str = "".join(
            line.serialize(newline=True) for line in context.pop((__tmp0, "lines"))
        )
        # TODO only feed dateutil the params it likes, add the rest as extra
        tzinfos = context.get(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        rrule = dateutil.rrule.rrulestr(lines_str, tzinfos=tzinfos, compatible=True)
        rrule._rdate = list(__tmp5(sorted(rrule._rdate)))  # type: ignore
        rrule._exdate = list(__tmp5(sorted(rrule._exdate)))  # type: ignore
        __tmp0.set_or_append_value(component, rrule)

    def serialize(__tmp0, component, __tmp1, context):
        value = __tmp0.get_value(component)
        if not TYPE_CHECKING:
            assert isinstance(value, dateutil.rrule.rruleset)
        for rrule in itertools.chain(value._rrule, value._exrule):
            if rrule._dtstart is None:
                continue
            # check that the rrule uses the same DTSTART as a possible Timespan(Converter)
            dtstart = context["DTSTART"]
            if dtstart:
                if dtstart != rrule._dtstart:
                    raise ValueError("differing DTSTART values")
            else:
                context["DTSTART"] = rrule._dtstart
                dt_value = DatetimeConverter.serialize(rrule._dtstart, context=context)
                __tmp1.append(ContentLine(name="DTSTART", value=dt_value))

        for rrule in value._rrule:
            __tmp1.append(rrule_to_ContentLine(rrule))
        for exrule in value._exrule:
            cl = rrule_to_ContentLine(exrule)
            cl.name = "EXRULE"
            __tmp1.append(cl)
        for rdate in __tmp5(sorted(value._rdate)):
            __tmp1.append(
                ContentLine(name="RDATE", value=DatetimeConverter.serialize(rdate))
            )
        for exdate in __tmp5(sorted(value._exdate)):
            __tmp1.append(
                ContentLine(name="EXDATE", value=DatetimeConverter.serialize(exdate))
            )

    def __tmp4(
        __tmp0, component, __tmp1: Container, context
    ):
        context.pop("DTSTART", None)


AttributeConverter.BY_TYPE[dateutil.rrule.rruleset] = __typ1


class __typ0(GenericConverter):
    CONTEXT_FIELD = "ALARM_ACTION"

    @property
    def priority(__tmp0) :
        return 1000

    @property
    def __tmp3(__tmp0) :
        return ["ACTION"]

    def __tmp2(
        __tmp0, component, item, context: __typ4
    ) -> __typ2:
        assert isinstance(item, ContentLine)
        assert issubclass(type(component), get_type_from_action(item.value))
        if item.params:
            component.extra_params["ACTION"] = copy_extra_params(item.params)
        return True

    def serialize(__tmp0, component, __tmp1: Container, context: __typ4):
        assert isinstance(component, BaseAlarm)
        __tmp1.append(
            ContentLine(
                name="ACTION",
                params=cast(ExtraParams, component.extra_params.get("ACTION", {})),
                value=component.action,
            )
        )


class AlarmMeta(ComponentMeta):
    def find_converters(__tmp0) :
        convs: List[GenericConverter] = [
            c
            for c in (
                AttributeConverter.get_converter_for(a)
                for a in attr.fields(__tmp0.component_type)
            )
            if c is not None
        ]
        convs.append(__typ0())
        return sort_converters(convs)

    def load_instance(
        __tmp0, container: <FILL>, context: Optional[__typ4] = None
    ):
        clazz = get_type_from_action(
            one(
                container["ACTION"],
                too_short="VALARM must have exactly one ACTION!",
                too_long="VALARM must have exactly one ACTION, but got {first!r}, {second!r}, and possibly more!",
            ).value
        )
        instance = clazz()
        ComponentMeta.BY_TYPE[clazz].populate_instance(instance, container, context)
        return instance


ComponentMeta.BY_TYPE[BaseAlarm] = AlarmMeta(BaseAlarm)
ComponentMeta.BY_TYPE[AudioAlarm] = AlarmMeta(AudioAlarm)
ComponentMeta.BY_TYPE[CustomAlarm] = AlarmMeta(CustomAlarm)
ComponentMeta.BY_TYPE[DisplayAlarm] = AlarmMeta(DisplayAlarm)
ComponentMeta.BY_TYPE[EmailAlarm] = AlarmMeta(EmailAlarm)
ComponentMeta.BY_TYPE[NoneAlarm] = AlarmMeta(NoneAlarm)
