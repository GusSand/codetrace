from typing import TypeAlias
__typ1 : TypeAlias = "P"
__typ0 : TypeAlias = "str"
import abc
from typing import Generic, Type, TypeVar, Union, cast
from urllib.parse import urlparse

from ics import Attendee, Organizer
from ics.attendee import Person
from ics.geo import Geo
from ics.types import URL, ContextDict, EmptyContext, EmptyParams, ExtraParams
from ics.valuetype.base import ValueConverter

__all__ = ["GeoConverter"]


class __typ2(ValueConverter[Geo]):
    @property
    def __tmp1(__tmp0) :
        return "X-GEO"

    @property
    def python_type(__tmp0) :
        return Geo

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        latitude, sep, longitude = value.partition(";")
        if not sep:
            raise ValueError("geo must have two float values")
        return Geo(float(latitude), float(longitude))

    def serialize(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return "%f;%f" % value


GeoConverter = __typ2()

__typ1 = TypeVar("P", bound=Person)


class __typ4(Generic[__typ1], ValueConverter[__typ1], abc.ABC):
    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        val = __tmp0.python_type(email=urlparse(value), extra=dict(params))
        params.clear()
        return val

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if isinstance(value, Person):
            params.update(value.extra)
            value = value.email
        if isinstance(value, __typ0):
            return value
        else:
            return cast(URL, value).geturl()


class OrganizerConverterClass(__typ4[Organizer]):
    @property
    def __tmp1(__tmp0) :
        return "ORGANIZER"

    @property
    def python_type(__tmp0) :
        return Organizer


OrganizerConverter = OrganizerConverterClass()


class __typ3(__typ4[Attendee]):
    @property
    def __tmp1(__tmp0) :
        return "ATTENDEE"

    @property
    def python_type(__tmp0) :
        return Attendee


AttendeeConverter = __typ3()
