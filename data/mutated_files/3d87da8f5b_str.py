from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ4 : TypeAlias = "URL"
__typ7 : TypeAlias = "bytes"
__typ5 : TypeAlias = "float"
__typ3 : TypeAlias = "bool"
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


class __typ2(ValueConverter[__typ7]):
    @property
    def __tmp3(__tmp0) :
        return "BINARY"

    @property
    def __tmp2(__tmp0) :
        return __typ7

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ7:
        return base64.b64decode(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return base64.b64encode(value).decode("ascii")


BinaryConverter = __typ2()
ValueConverter.BY_TYPE[bytearray] = ValueConverter.BY_TYPE[__typ7]


class BooleanConverterClass(ValueConverter[__typ3]):
    @property
    def __tmp3(__tmp0) :
        return "BOOLEAN"

    @property
    def __tmp2(__tmp0) :
        return __typ3

    def parse(
        __tmp0,
        value: str,
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

    def __tmp1(
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


class __typ6(ValueConverter[__typ0]):
    @property
    def __tmp3(__tmp0) :
        return "INTEGER"

    @property
    def __tmp2(__tmp0) :
        return __typ0

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return __typ0(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return str(value)


IntegerConverter = __typ6()


class FloatConverterClass(ValueConverter[__typ5]):
    @property
    def __tmp3(__tmp0) :
        return "FLOAT"

    @property
    def __tmp2(__tmp0) :
        return __typ5

    def parse(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ5:
        return __typ5(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return str(value)


FloatConverter = FloatConverterClass()


class __typ1(ValueConverter[__typ4]):
    # TODO URI PARAMs need percent escaping, preventing all illegal characters except for ", in which they also need to wrapped
    # TODO URI values also need percent escaping (escaping COMMA characters in URI Lists), but no quoting

    @property
    def __tmp3(__tmp0) :
        return "URI"

    @property
    def __tmp2(__tmp0) :
        return __typ4

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return urlparse(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if isinstance(value, str):
            return value
        else:
            return value.geturl()


URIConverter = __typ1()


class CalendarUserAddressConverterClass(__typ1):
    @property
    def __tmp3(__tmp0) :
        return "CAL-ADDRESS"


CalendarUserAddressConverter = CalendarUserAddressConverterClass
