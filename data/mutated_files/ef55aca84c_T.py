from typing import TypeAlias
__typ1 : TypeAlias = "str"
import abc
from typing import Dict, Generic, Iterable, Type, TypeVar

from ics.types import ContextDict, EmptyContext, EmptyParams, ExtraParams

T = TypeVar("T")

__all__ = ["ValueConverter"]


class __typ0(Generic[T], abc.ABC):
    BY_NAME: Dict[__typ1, "ValueConverter"] = {}
    BY_TYPE: Dict[Type, "ValueConverter"] = {}

    def __tmp2(__tmp0):
        __typ0.BY_NAME[__tmp0.ics_type] = __tmp0
        __typ0.BY_TYPE.setdefault(__tmp0.python_type, __tmp0)

    @property
    @abc.abstractmethod
    def ics_type(__tmp0) :
        ...

    @property
    @abc.abstractmethod
    def python_type(__tmp0) :
        ...

    def split_value_list(__tmp0, __tmp3) :
        yield from __tmp3.split(",")

    def join_value_list(__tmp0, __tmp3) :
        return ",".join(__tmp3)

    @abc.abstractmethod
    def __tmp6(
        __tmp0,
        __tmp1,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        ...

    @abc.abstractmethod
    def __tmp4(
        __tmp0,
        __tmp1: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        ...

    def __tmp5(__tmp0):
        return "<" + __tmp0.__class__.__name__ + ">"

    def __hash__(__tmp0):
        return hash(type(__tmp0))
