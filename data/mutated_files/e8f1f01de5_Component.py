from typing import TypeAlias
__typ0 : TypeAlias = "ContainerItem"
__typ1 : TypeAlias = "ContextDict"
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


def unique_justseen(iterable, key=None):
    return map(next, map(operator.itemgetter(1), itertools.groupby(iterable, key)))


class RecurrenceConverter(AttributeConverter):
    @property
    def filter_ics_names(__tmp1) -> List[str]:
        return ["RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]

    def populate(
        __tmp1, component: Component, __tmp2: __typ0, __tmp0
    ) :
        assert isinstance(__tmp2, ContentLine)
        key = (__tmp1, "lines")
        lines = __tmp0[key]
        if lines is None:
            lines = __tmp0[key] = []
        lines.append(__tmp2)
        return True

    def post_populate(__tmp1, component, __tmp0: __typ1):
        lines_str = "".join(
            line.serialize(newline=True) for line in __tmp0.pop((__tmp1, "lines"))
        )
        # TODO only feed dateutil the params it likes, add the rest as extra
        tzinfos = __tmp0.get(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        rrule = dateutil.rrule.rrulestr(lines_str, tzinfos=tzinfos, compatible=True)
        rrule._rdate = list(unique_justseen(sorted(rrule._rdate)))  # type: ignore
        rrule._exdate = list(unique_justseen(sorted(rrule._exdate)))  # type: ignore
        __tmp1.set_or_append_value(component, rrule)

    def serialize(__tmp1, component: Component, output: Container, __tmp0):
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
        for rdate in unique_justseen(sorted(value._rdate)):
            output.append(
                ContentLine(name="RDATE", value=DatetimeConverter.serialize(rdate))
            )
        for exdate in unique_justseen(sorted(value._exdate)):
            output.append(
                ContentLine(name="EXDATE", value=DatetimeConverter.serialize(exdate))
            )

    def post_serialize(
        __tmp1, component: Component, output, __tmp0
    ):
        __tmp0.pop("DTSTART", None)


AttributeConverter.BY_TYPE[dateutil.rrule.rruleset] = RecurrenceConverter


class AlarmActionConverter(GenericConverter):
    CONTEXT_FIELD = "ALARM_ACTION"

    @property
    def priority(__tmp1) :
        return 1000

    @property
    def filter_ics_names(__tmp1) :
        return ["ACTION"]

    def populate(
        __tmp1, component: <FILL>, __tmp2: __typ0, __tmp0
    ) :
        assert isinstance(__tmp2, ContentLine)
        assert issubclass(type(component), get_type_from_action(__tmp2.value))
        if __tmp2.params:
            component.extra_params["ACTION"] = copy_extra_params(__tmp2.params)
        return True

    def serialize(__tmp1, component: Component, output: Container, __tmp0: __typ1):
        assert isinstance(component, BaseAlarm)
        output.append(
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
        convs.append(AlarmActionConverter())
        return sort_converters(convs)

    def load_instance(
        __tmp1, container: Container, __tmp0: Optional[__typ1] = None
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
