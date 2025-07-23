from typing import TypeAlias
__typ9 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "str"
__typ7 : TypeAlias = "URL"
__typ6 : TypeAlias = "bool"
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


class __typ4(ValueConverter[__typ9]):
    @property
    def __tmp3(__tmp0) -> __typ3:
        return "BINARY"

    @property
    def __tmp2(__tmp0) -> Type[__typ9]:
        return __typ9

    def parse(
        __tmp0,
        value: __typ3,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ9:
        return base64.b64decode(value)

    def __tmp1(
        __tmp0,
        value: __typ9,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return base64.b64encode(value).decode("ascii")


BinaryConverter = __typ4()
ValueConverter.BY_TYPE[bytearray] = ValueConverter.BY_TYPE[__typ9]


class __typ10(ValueConverter[__typ6]):
    @property
    def __tmp3(__tmp0) -> __typ3:
        return "BOOLEAN"

    @property
    def __tmp2(__tmp0) -> Type[__typ6]:
        return __typ6

    def parse(
        __tmp0,
        value: __typ3,
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
    ) -> __typ3:
        if isinstance(value, __typ3):
            value = __tmp0.parse(value, params, context)
        if value:
            return "TRUE"
        else:
            return "FALSE"


BooleanConverter = __typ10()


class __typ8(ValueConverter[__typ0]):
    @property
    def __tmp3(__tmp0) -> __typ3:
        return "INTEGER"

    @property
    def __tmp2(__tmp0) -> Type[__typ0]:
        return __typ0

    def parse(
        __tmp0,
        value: __typ3,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ0:
        return __typ0(value)

    def __tmp1(
        __tmp0,
        value: __typ0,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return __typ3(value)


IntegerConverter = __typ8()


class __typ5(ValueConverter[float]):
    @property
    def __tmp3(__tmp0) -> __typ3:
        return "FLOAT"

    @property
    def __tmp2(__tmp0) -> Type[float]:
        return float

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> float:
        return float(value)

    def __tmp1(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ3:
        return __typ3(value)


FloatConverter = __typ5()


class __typ2(ValueConverter[__typ7]):
    # TODO URI PARAMs need percent escaping, preventing all illegal characters except for ", in which they also need to wrapped
    # TODO URI values also need percent escaping (escaping COMMA characters in URI Lists), but no quoting

    @property
    def __tmp3(__tmp0) :
        return "URI"

    @property
    def __tmp2(__tmp0) -> Type[__typ7]:
        return __typ7

    def parse(
        __tmp0,
        value: __typ3,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ7:
        return urlparse(value)

    def __tmp1(
        __tmp0,
        value: __typ7,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ3:
        if isinstance(value, __typ3):
            return value
        else:
            return value.geturl()


URIConverter = __typ2()


class __typ1(__typ2):
    @property
    def __tmp3(__tmp0) -> __typ3:
        return "CAL-ADDRESS"


CalendarUserAddressConverter = __typ1
