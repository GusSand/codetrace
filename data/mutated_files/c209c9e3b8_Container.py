from typing import TypeAlias
__typ0 : TypeAlias = "ContextDict"
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


def __tmp8(__tmp5, key=None):
    return map(next, map(operator.itemgetter(1), itertools.groupby(__tmp5, key)))


class RecurrenceConverter(AttributeConverter):
    @property
    def __tmp6(__tmp1) -> List[str]:
        return ["RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]

    def populate(
        __tmp1, component: Component, __tmp3: ContainerItem, context: __typ0
    ) -> bool:
        assert isinstance(__tmp3, ContentLine)
        key = (__tmp1, "lines")
        lines = context[key]
        if lines is None:
            lines = context[key] = []
        lines.append(__tmp3)
        return True

    def post_populate(__tmp1, component, context: __typ0):
        lines_str = "".join(
            line.serialize(newline=True) for line in context.pop((__tmp1, "lines"))
        )
        # TODO only feed dateutil the params it likes, add the rest as extra
        tzinfos = context.get(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        rrule = dateutil.rrule.rrulestr(lines_str, tzinfos=tzinfos, compatible=True)
        rrule._rdate = list(__tmp8(sorted(rrule._rdate)))  # type: ignore
        rrule._exdate = list(__tmp8(sorted(rrule._exdate)))  # type: ignore
        __tmp1.set_or_append_value(component, rrule)

    def serialize(__tmp1, component, __tmp2: <FILL>, context: __typ0):
        value = __tmp1.get_value(component)
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
                __tmp2.append(ContentLine(name="DTSTART", value=dt_value))

        for rrule in value._rrule:
            __tmp2.append(rrule_to_ContentLine(rrule))
        for exrule in value._exrule:
            cl = rrule_to_ContentLine(exrule)
            cl.name = "EXRULE"
            __tmp2.append(cl)
        for rdate in __tmp8(sorted(value._rdate)):
            __tmp2.append(
                ContentLine(name="RDATE", value=DatetimeConverter.serialize(rdate))
            )
        for exdate in __tmp8(sorted(value._exdate)):
            __tmp2.append(
                ContentLine(name="EXDATE", value=DatetimeConverter.serialize(exdate))
            )

    def __tmp7(
        __tmp1, component, __tmp2, context: __typ0
    ):
        context.pop("DTSTART", None)


AttributeConverter.BY_TYPE[dateutil.rrule.rruleset] = RecurrenceConverter


class __typ1(GenericConverter):
    CONTEXT_FIELD = "ALARM_ACTION"

    @property
    def priority(__tmp1) -> int:
        return 1000

    @property
    def __tmp6(__tmp1) -> List[str]:
        return ["ACTION"]

    def populate(
        __tmp1, component: Component, __tmp3: ContainerItem, context: __typ0
    ) -> bool:
        assert isinstance(__tmp3, ContentLine)
        assert issubclass(type(component), get_type_from_action(__tmp3.value))
        if __tmp3.params:
            component.extra_params["ACTION"] = copy_extra_params(__tmp3.params)
        return True

    def serialize(__tmp1, component: Component, __tmp2: Container, context: __typ0):
        assert isinstance(component, BaseAlarm)
        __tmp2.append(
            ContentLine(
                name="ACTION",
                params=cast(ExtraParams, component.extra_params.get("ACTION", {})),
                value=component.action,
            )
        )


class AlarmMeta(ComponentMeta):
    def find_converters(__tmp1) -> Iterable[GenericConverter]:
        convs: List[GenericConverter] = [
            c
            for c in (
                AttributeConverter.get_converter_for(a)
                for a in attr.fields(__tmp1.component_type)
            )
            if c is not None
        ]
        convs.append(__typ1())
        return sort_converters(convs)

    def __tmp4(
        __tmp1, __tmp0: Container, context: Optional[__typ0] = None
    ):
        clazz = get_type_from_action(
            one(
                __tmp0["ACTION"],
                too_short="VALARM must have exactly one ACTION!",
                too_long="VALARM must have exactly one ACTION, but got {first!r}, {second!r}, and possibly more!",
            ).value
        )
        instance = clazz()
        ComponentMeta.BY_TYPE[clazz].populate_instance(instance, __tmp0, context)
        return instance


ComponentMeta.BY_TYPE[BaseAlarm] = AlarmMeta(BaseAlarm)
ComponentMeta.BY_TYPE[AudioAlarm] = AlarmMeta(AudioAlarm)
ComponentMeta.BY_TYPE[CustomAlarm] = AlarmMeta(CustomAlarm)
ComponentMeta.BY_TYPE[DisplayAlarm] = AlarmMeta(DisplayAlarm)
ComponentMeta.BY_TYPE[EmailAlarm] = AlarmMeta(EmailAlarm)
ComponentMeta.BY_TYPE[NoneAlarm] = AlarmMeta(NoneAlarm)
