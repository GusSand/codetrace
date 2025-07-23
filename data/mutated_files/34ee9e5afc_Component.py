from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "bool"
__typ4 : TypeAlias = "Container"
__typ7 : TypeAlias = "ContextDict"
__typ6 : TypeAlias = "ContainerItem"
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


class __typ2(AttributeConverter):
    @property
    def filter_ics_names(__tmp1) -> List[str]:
        return ["RRULE", "RDATE", "EXRULE", "EXDATE", "DTSTART"]

    def __tmp5(
        __tmp1, component: <FILL>, __tmp4: __typ6, __tmp0: __typ7
    ) -> __typ5:
        assert isinstance(__tmp4, ContentLine)
        key = (__tmp1, "lines")
        lines = __tmp0[key]
        if lines is None:
            lines = __tmp0[key] = []
        lines.append(__tmp4)
        return True

    def __tmp7(__tmp1, component: Component, __tmp0: __typ7):
        lines_str = "".join(
            line.serialize(newline=True) for line in __tmp0.pop((__tmp1, "lines"))
        )
        # TODO only feed dateutil the params it likes, add the rest as extra
        tzinfos = __tmp0.get(DatetimeConverterMixin.CONTEXT_KEY_AVAILABLE_TZ, {})
        rrule = dateutil.rrule.rrulestr(lines_str, tzinfos=tzinfos, compatible=True)
        rrule._rdate = list(unique_justseen(sorted(rrule._rdate)))  # type: ignore
        rrule._exdate = list(unique_justseen(sorted(rrule._exdate)))  # type: ignore
        __tmp1.set_or_append_value(component, rrule)

    def serialize(__tmp1, component: Component, __tmp3: __typ4, __tmp0: __typ7):
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
        for rdate in unique_justseen(sorted(value._rdate)):
            __tmp3.append(
                ContentLine(name="RDATE", value=DatetimeConverter.serialize(rdate))
            )
        for exdate in unique_justseen(sorted(value._exdate)):
            __tmp3.append(
                ContentLine(name="EXDATE", value=DatetimeConverter.serialize(exdate))
            )

    def __tmp8(
        __tmp1, component: Component, __tmp3, __tmp0
    ):
        __tmp0.pop("DTSTART", None)


AttributeConverter.BY_TYPE[dateutil.rrule.rruleset] = __typ2


class __typ1(GenericConverter):
    CONTEXT_FIELD = "ALARM_ACTION"

    @property
    def __tmp6(__tmp1) -> __typ0:
        return 1000

    @property
    def filter_ics_names(__tmp1) :
        return ["ACTION"]

    def __tmp5(
        __tmp1, component: Component, __tmp4, __tmp0: __typ7
    ) -> __typ5:
        assert isinstance(__tmp4, ContentLine)
        assert issubclass(type(component), get_type_from_action(__tmp4.value))
        if __tmp4.params:
            component.extra_params["ACTION"] = copy_extra_params(__tmp4.params)
        return True

    def serialize(__tmp1, component: Component, __tmp3, __tmp0):
        assert isinstance(component, BaseAlarm)
        __tmp3.append(
            ContentLine(
                name="ACTION",
                params=cast(ExtraParams, component.extra_params.get("ACTION", {})),
                value=component.action,
            )
        )


class __typ3(ComponentMeta):
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

    def load_instance(
        __tmp1, __tmp2: __typ4, __tmp0: Optional[__typ7] = None
    ):
        clazz = get_type_from_action(
            one(
                __tmp2["ACTION"],
                too_short="VALARM must have exactly one ACTION!",
                too_long="VALARM must have exactly one ACTION, but got {first!r}, {second!r}, and possibly more!",
            ).value
        )
        instance = clazz()
        ComponentMeta.BY_TYPE[clazz].populate_instance(instance, __tmp2, __tmp0)
        return instance


ComponentMeta.BY_TYPE[BaseAlarm] = __typ3(BaseAlarm)
ComponentMeta.BY_TYPE[AudioAlarm] = __typ3(AudioAlarm)
ComponentMeta.BY_TYPE[CustomAlarm] = __typ3(CustomAlarm)
ComponentMeta.BY_TYPE[DisplayAlarm] = __typ3(DisplayAlarm)
ComponentMeta.BY_TYPE[EmailAlarm] = __typ3(EmailAlarm)
ComponentMeta.BY_TYPE[NoneAlarm] = __typ3(NoneAlarm)
