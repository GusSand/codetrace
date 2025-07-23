from typing import TypeAlias
__typ1 : TypeAlias = "T"
import abc
from typing import Dict, Generic, Iterable, Type, TypeVar

from ics.types import ContextDict, EmptyContext, EmptyParams, ExtraParams

__typ1 = TypeVar("T")

__all__ = ["ValueConverter"]


class __typ0(Generic[__typ1], abc.ABC):
    BY_NAME: Dict[str, "ValueConverter"] = {}
    BY_TYPE: Dict[Type, "ValueConverter"] = {}

    def __tmp3(__tmp0):
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

    def split_value_list(__tmp0, __tmp4: <FILL>) -> Iterable[str]:
        yield from __tmp4.split(",")

    def __tmp2(__tmp0, __tmp4) :
        return ",".join(__tmp4)

    @abc.abstractmethod
    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        ...

    @abc.abstractmethod
    def __tmp5(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        ...

    def __str__(__tmp0):
        return "<" + __tmp0.__class__.__name__ + ">"

    def __tmp1(__tmp0):
        return hash(type(__tmp0))
