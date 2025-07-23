import base64
from typing import Type, Union
from urllib.parse import urlparse

from ics.types import URL, ContextDict, EmptyContext, EmptyParams, ExtraParams
from ics.valuetype.base import ValueConverter

__all__ = [
    "BinaryConverter",
    "BooleanConverter",
    "IntegerConverter",
    "FloatConverter",
    "URIConverter",
    "CalendarUserAddressConverter",
]


class BinaryConverterClass(ValueConverter[bytes]):
    @property
    def __tmp2(__tmp0) :
        return "BINARY"

    @property
    def __tmp1(__tmp0) :
        return bytes

    def parse(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return base64.b64decode(value)

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return base64.b64encode(value).decode("ascii")


BinaryConverter = BinaryConverterClass()
ValueConverter.BY_TYPE[bytearray] = ValueConverter.BY_TYPE[bytes]


class BooleanConverterClass(ValueConverter[bool]):
    @property
    def __tmp2(__tmp0) :
        return "BOOLEAN"

    @property
    def __tmp1(__tmp0) :
        return bool

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if value == "TRUE":
            return True
        elif value == "FALSE":
            return False
        else:
            value = value.upper()
            if value == "TRUE":
                return True
            elif value == "FALSE":
                return False
            elif value in ["T", "Y", "YES", "ON", "1"]:
                return True
            elif value in ["F", "N", "NO", "OFF", "0"]:
                return False
            else:
                raise ValueError(f"can't interpret '{value}' as boolean")

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if isinstance(value, str):
            value = __tmp0.parse(value, params, context)
        if value:
            return "TRUE"
        else:
            return "FALSE"


BooleanConverter = BooleanConverterClass()


class IntegerConverterClass(ValueConverter[int]):
    @property
    def __tmp2(__tmp0) :
        return "INTEGER"

    @property
    def __tmp1(__tmp0) :
        return int

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return int(value)

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return str(value)


IntegerConverter = IntegerConverterClass()


class FloatConverterClass(ValueConverter[float]):
    @property
    def __tmp2(__tmp0) :
        return "FLOAT"

    @property
    def __tmp1(__tmp0) :
        return float

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return float(value)

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return str(value)


FloatConverter = FloatConverterClass()


class URIConverterClass(ValueConverter[URL]):
    # TODO URI PARAMs need percent escaping, preventing all illegal characters except for ", in which they also need to wrapped
    # TODO URI values also need percent escaping (escaping COMMA characters in URI Lists), but no quoting

    @property
    def __tmp2(__tmp0) :
        return "URI"

    @property
    def __tmp1(__tmp0) :
        return URL

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return urlparse(value)

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if isinstance(value, str):
            return value
        else:
            return value.geturl()


URIConverter = URIConverterClass()


class CalendarUserAddressConverterClass(URIConverterClass):
    @property
    def __tmp2(__tmp0) :
        return "CAL-ADDRESS"


CalendarUserAddressConverter = CalendarUserAddressConverterClass
