from typing import Any, Dict, Generic, Iterable, List, TypeVar

import attr

from ics.utils import check_is_instance
from ics.valuetype.base import ValueConverter
from ics.valuetype.generic import BooleanConverter, URIConverter
from ics.valuetype.text import RawTextConverter

T = TypeVar("T")


@attr.s(frozen=True)
class __typ1(Generic[T]):
    name: str = attr.ib()
    converter: ValueConverter[T] = attr.ib(default=RawTextConverter)
    default: Any = attr.ib(default=None)

    def __tmp2(__tmp0, instance: "Person", __tmp1) -> T:
        if __tmp0.name not in instance.extra:
            return __tmp0.default
        value = instance.extra[__tmp0.name]
        if len(value) == 0:
            return __tmp0.default
        elif len(value) == 1:
            return __tmp0.converter.parse(value[0])
        else:
            raise ValueError(
                f"Expected at most one value for property {__tmp0.name!r}, got {value!r}!"
            )

    def __tmp4(__tmp0, instance, value: <FILL>):
        instance.extra[__tmp0.name] = [__tmp0.converter.serialize(value)]

    def __tmp3(__tmp0, instance):
        instance.extra.pop(__tmp0.name, None)


@attr.s(frozen=True)
class __typ3(Generic[T]):
    name: str = attr.ib()
    converter: ValueConverter[T] = attr.ib(default=RawTextConverter)
    default: Any = attr.ib(default=None)

    def __tmp2(__tmp0, instance, __tmp1) -> List[T]:
        if __tmp0.name not in instance.extra:
            return __tmp0.default
        return [__tmp0.converter.parse(v) for v in instance.extra[__tmp0.name]]

    def __tmp4(__tmp0, instance, value):
        instance.extra[__tmp0.name] = [__tmp0.converter.serialize(v) for v in value]

    def __tmp3(__tmp0, instance: "Person"):
        instance.extra.pop(__tmp0.name, None)


@attr.s
class __typ2:
    email: str = attr.ib()
    extra: Dict[str, List[str]] = attr.ib(factory=dict)


class __typ0(__typ2):
    """Abstract class for Attendee and Organizer."""

    NAME = "ABSTRACT-PERSON"

    def __init__(__tmp0, email, extra=None, **kwargs):
        if extra is None:
            extra = dict()
        else:
            check_is_instance("extra", extra, dict)
        super().__init__(email, extra)
        for key, val in kwargs.items():
            setattr(__tmp0, key, val)

    sent_by = __typ1("SENT-BY", URIConverter)
    common_name = __typ1[str]("CN")
    directory = __typ1("DIR", URIConverter)


class Organizer(__typ0):
    """Organizer of an event or todo."""

    NAME = "ORGANIZER"


class __typ4(__typ0):
    """Attendee of an event or todo.

    Possible values according to iCalendar standard, first value is default:
        user_type = INDIVIDUAL | GROUP | RESOURCE | ROOM | UNKNOWN
        member = Person
        role = REQ-PARTICIPANT | CHAIR | OPT-PARTICIPANT | NON-PARTICIPANT
        rsvp = False | True
        delegated_to = Person
        delegated_from = Person

        Depending on the Component, different status are possible.
        Event:
        status = NEEDS-ACTION | ACCEPTED | DECLINED | TENTATIVE | DELEGATED
        Todo:
        status = NEEDS-ACTION | ACCEPTED | DECLINED | TENTATIVE | DELEGATED | COMPLETED | IN-PROCESS
    """

    NAME = "ATTENDEE"

    user_type = __typ1[str]("CUTYPE", default="INDIVIDUAL")
    member = __typ3("MEMBER", converter=URIConverter)
    role = __typ1[str]("ROLE", default="REQ-PARTICIPANT")
    status = __typ1[str]("PARTSTAT", default="NEEDS-ACTION")
    rsvp = __typ1("RSVP", converter=BooleanConverter, default=False)
    delegated_to = __typ3("DELEGATED-TO", converter=URIConverter)
    delegated_from = __typ3("DELEGATED-FROM", converter=URIConverter)
