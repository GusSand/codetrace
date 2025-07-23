from typing import TypeAlias
__typ2 : TypeAlias = "dict"
__typ4 : TypeAlias = "Event"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event


class __typ1(metaclass=ABCMeta):
    """
    Interface for storage methods.
    """

    sid = "Storage id not set, fix me"

    @abstractmethod
    def __tmp12(__tmp0, testing: __typ3) -> None:
        __tmp0.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp17(__tmp0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
        __tmp0,
        __tmp1: str,
        __tmp20: str,
        __tmp13: str,
        __tmp14: str,
        __tmp9,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp0,
        __tmp1: <FILL>,
        __tmp20: Optional[str] = None,
        __tmp13: Optional[str] = None,
        __tmp14: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp16(__tmp0, __tmp1) :
        raise NotImplementedError

    @abstractmethod
    def __tmp6(__tmp0, __tmp1: str) :
        raise NotImplementedError

    @abstractmethod
    def __tmp22(
        __tmp0,
        __tmp1: str,
        __tmp4,
    ) -> Optional[__typ4]:
        raise NotImplementedError

    @abstractmethod
    def __tmp19(
        __tmp0,
        __tmp1: str,
        __tmp10: __typ0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ4]:
        raise NotImplementedError

    def __tmp7(
        __tmp0,
        __tmp1: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp0, __tmp1: str, __tmp2) -> __typ4:
        raise NotImplementedError

    def __tmp15(__tmp0, __tmp1, __tmp21: List[__typ4]) -> None:
        for __tmp2 in __tmp21:
            __tmp0.insert_one(__tmp1, __tmp2)

    @abstractmethod
    def __tmp8(__tmp0, __tmp1: str, __tmp4: __typ0) -> __typ3:
        raise NotImplementedError

    @abstractmethod
    def __tmp18(__tmp0, __tmp1: str, __tmp4: __typ0, __tmp2: __typ4) :
        raise NotImplementedError

    @abstractmethod
    def __tmp11(__tmp0, __tmp1: str, __tmp2) -> None:
        raise NotImplementedError
