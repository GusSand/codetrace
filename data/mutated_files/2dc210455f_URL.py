from typing import TypeAlias
__typ6 : TypeAlias = "float"
__typ0 : TypeAlias = "int"
__typ5 : TypeAlias = "bool"
__typ2 : TypeAlias = "str"
__typ8 : TypeAlias = "bytes"
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


class __typ3(ValueConverter[__typ8]):
    @property
    def __tmp3(__tmp0) -> __typ2:
        return "BINARY"

    @property
    def __tmp2(__tmp0) -> Type[__typ8]:
        return __typ8

    def parse(
        __tmp0,
        value: __typ2,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ8:
        return base64.b64decode(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ2:
        return base64.b64encode(value).decode("ascii")


BinaryConverter = __typ3()
ValueConverter.BY_TYPE[bytearray] = ValueConverter.BY_TYPE[__typ8]


class __typ9(ValueConverter[__typ5]):
    @property
    def __tmp3(__tmp0) -> __typ2:
        return "BOOLEAN"

    @property
    def __tmp2(__tmp0) -> Type[__typ5]:
        return __typ5

    def parse(
        __tmp0,
        value: __typ2,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ5:
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
        if isinstance(value, __typ2):
            value = __tmp0.parse(value, params, context)
        if value:
            return "TRUE"
        else:
            return "FALSE"


BooleanConverter = __typ9()


class __typ7(ValueConverter[__typ0]):
    @property
    def __tmp3(__tmp0) -> __typ2:
        return "INTEGER"

    @property
    def __tmp2(__tmp0) -> Type[__typ0]:
        return __typ0

    def parse(
        __tmp0,
        value: __typ2,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ0:
        return __typ0(value)

    def __tmp1(
        __tmp0,
        value: __typ0,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ2:
        return __typ2(value)


IntegerConverter = __typ7()


class __typ4(ValueConverter[__typ6]):
    @property
    def __tmp3(__tmp0) -> __typ2:
        return "FLOAT"

    @property
    def __tmp2(__tmp0) :
        return __typ6

    def parse(
        __tmp0,
        value: __typ2,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return __typ6(value)

    def __tmp1(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return __typ2(value)


FloatConverter = __typ4()


class __typ1(ValueConverter[URL]):
    # TODO URI PARAMs need percent escaping, preventing all illegal characters except for ", in which they also need to wrapped
    # TODO URI values also need percent escaping (escaping COMMA characters in URI Lists), but no quoting

    @property
    def __tmp3(__tmp0) -> __typ2:
        return "URI"

    @property
    def __tmp2(__tmp0) -> Type[URL]:
        return URL

    def parse(
        __tmp0,
        value: __typ2,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> URL:
        return urlparse(value)

    def __tmp1(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ2:
        if isinstance(value, __typ2):
            return value
        else:
            return value.geturl()


URIConverter = __typ1()


class CalendarUserAddressConverterClass(__typ1):
    @property
    def __tmp3(__tmp0) -> __typ2:
        return "CAL-ADDRESS"


CalendarUserAddressConverter = CalendarUserAddressConverterClass
