import abc
from typing import Generic, Type, TypeVar, Union, cast
from urllib.parse import urlparse

from ics import Attendee, Organizer
from ics.attendee import Person
from ics.geo import Geo
from ics.types import URL, ContextDict, EmptyContext, EmptyParams, ExtraParams
from ics.valuetype.base import ValueConverter

__all__ = ["GeoConverter"]


class GeoConverterClass(ValueConverter[Geo]):
    @property
    def __tmp2(__tmp0) :
        return "X-GEO"

    @property
    def python_type(__tmp0) -> Type[Geo]:
        return Geo

    def parse(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        latitude, sep, longitude = value.partition(";")
        if not sep:
            raise ValueError("geo must have two float values")
        return Geo(float(latitude), float(longitude))

    def __tmp1(
        __tmp0,
        value: Geo,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return "%f;%f" % value


GeoConverter = GeoConverterClass()

P = TypeVar("P", bound=Person)


class PersonConverter(Generic[P], ValueConverter[P], abc.ABC):
    def parse(
        __tmp0,
        value: str,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> P:
        val = __tmp0.python_type(email=urlparse(value), extra=dict(params))
        params.clear()
        return val

    def __tmp1(
        __tmp0,
        value: Union[P, str],
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        if isinstance(value, Person):
            params.update(value.extra)
            value = value.email
        if isinstance(value, str):
            return value
        else:
            return cast(URL, value).geturl()


class OrganizerConverterClass(PersonConverter[Organizer]):
    @property
    def __tmp2(__tmp0) -> str:
        return "ORGANIZER"

    @property
    def python_type(__tmp0) -> Type[Organizer]:
        return Organizer


OrganizerConverter = OrganizerConverterClass()


class __typ0(PersonConverter[Attendee]):
    @property
    def __tmp2(__tmp0) -> str:
        return "ATTENDEE"

    @property
    def python_type(__tmp0) :
        return Attendee


AttendeeConverter = __typ0()
