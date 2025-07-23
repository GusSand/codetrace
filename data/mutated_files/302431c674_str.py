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
    def __tmp2(__tmp0) -> str:
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

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return "%f;%f" % value


GeoConverter = GeoConverterClass()

P = TypeVar("P", bound=Person)


class __typ0(Generic[P], ValueConverter[P], abc.ABC):
    def parse(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        val = __tmp0.python_type(email=urlparse(value), extra=dict(params))
        params.clear()
        return val

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if isinstance(value, Person):
            params.update(value.extra)
            value = value.email
        if isinstance(value, str):
            return value
        else:
            return cast(URL, value).geturl()


class OrganizerConverterClass(__typ0[Organizer]):
    @property
    def __tmp2(__tmp0) -> str:
        return "ORGANIZER"

    @property
    def python_type(__tmp0) :
        return Organizer


OrganizerConverter = OrganizerConverterClass()


class AttendeeConverterClass(__typ0[Attendee]):
    @property
    def __tmp2(__tmp0) :
        return "ATTENDEE"

    @property
    def python_type(__tmp0) :
        return Attendee


AttendeeConverter = AttendeeConverterClass()
