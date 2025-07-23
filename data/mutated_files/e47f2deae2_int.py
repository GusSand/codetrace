from typing import TypeAlias
__typ3 : TypeAlias = "bool"
__typ5 : TypeAlias = "float"
__typ4 : TypeAlias = "URL"
__typ1 : TypeAlias = "str"
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
    def __tmp3(__tmp0) -> __typ1:
        return "BINARY"

    @property
    def __tmp2(__tmp0) -> Type[bytes]:
        return bytes

    def parse(
        __tmp0,
        value: __typ1,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return base64.b64decode(value)

    def __tmp1(
        __tmp0,
        value: bytes,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return base64.b64encode(value).decode("ascii")


BinaryConverter = BinaryConverterClass()
ValueConverter.BY_TYPE[bytearray] = ValueConverter.BY_TYPE[bytes]


class __typ6(ValueConverter[__typ3]):
    @property
    def __tmp3(__tmp0) -> __typ1:
        return "BOOLEAN"

    @property
    def __tmp2(__tmp0) :
        return __typ3

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

    def __tmp1(
        __tmp0,
        value: Union[__typ3, __typ1],
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ1:
        if isinstance(value, __typ1):
            value = __tmp0.parse(value, params, context)
        if value:
            return "TRUE"
        else:
            return "FALSE"


BooleanConverter = __typ6()


class IntegerConverterClass(ValueConverter[int]):
    @property
    def __tmp3(__tmp0) :
        return "INTEGER"

    @property
    def __tmp2(__tmp0) :
        return int

    def parse(
        __tmp0,
        value: __typ1,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return int(value)

    def __tmp1(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ1:
        return __typ1(value)


IntegerConverter = IntegerConverterClass()


class __typ2(ValueConverter[__typ5]):
    @property
    def __tmp3(__tmp0) :
        return "FLOAT"

    @property
    def __tmp2(__tmp0) -> Type[__typ5]:
        return __typ5

    def parse(
        __tmp0,
        value: __typ1,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ5:
        return __typ5(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ1:
        return __typ1(value)


FloatConverter = __typ2()


class URIConverterClass(ValueConverter[__typ4]):
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
    ) -> __typ4:
        return urlparse(value)

    def __tmp1(
        __tmp0,
        value: __typ4,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        if isinstance(value, __typ1):
            return value
        else:
            return value.geturl()


URIConverter = URIConverterClass()


class __typ0(URIConverterClass):
    @property
    def __tmp3(__tmp0) -> __typ1:
        return "CAL-ADDRESS"


CalendarUserAddressConverter = __typ0
