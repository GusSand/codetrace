from typing import TypeAlias
__typ0 : TypeAlias = "T"
import abc
from typing import Dict, Generic, Iterable, Type, TypeVar

from ics.types import ContextDict, EmptyContext, EmptyParams, ExtraParams

__typ0 = TypeVar("T")

__all__ = ["ValueConverter"]


class ValueConverter(Generic[__typ0], abc.ABC):
    BY_NAME: Dict[str, "ValueConverter"] = {}
    BY_TYPE: Dict[Type, "ValueConverter"] = {}

    def __tmp5(__tmp0):
        ValueConverter.BY_NAME[__tmp0.ics_type] = __tmp0
        ValueConverter.BY_TYPE.setdefault(__tmp0.python_type, __tmp0)

    @property
    @abc.abstractmethod
    def ics_type(__tmp0) -> str:
        ...

    @property
    @abc.abstractmethod
    def python_type(__tmp0) -> Type[__typ0]:
        ...

    def __tmp3(__tmp0, __tmp6) :
        yield from __tmp6.split(",")

    def __tmp4(__tmp0, __tmp6: Iterable[str]) :
        return ",".join(__tmp6)

    @abc.abstractmethod
    def __tmp9(
        __tmp0,
        __tmp1: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> __typ0:
        ...

    @abc.abstractmethod
    def __tmp7(
        __tmp0,
        __tmp1,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        ...

    def __tmp8(__tmp0):
        return "<" + __tmp0.__class__.__name__ + ">"

    def __tmp2(__tmp0):
        return hash(type(__tmp0))
