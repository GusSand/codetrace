from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
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
    def __tmp11(__tmp0, testing: __typ4) :
        __tmp0.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp15(__tmp0) -> Dict[__typ2, __typ3]:
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
        __tmp0,
        __tmp1: __typ2,
        __tmp18,
        __tmp12: __typ2,
        __tmp13: __typ2,
        __tmp8: __typ2,
        name: Optional[__typ2] = None,
        data: Optional[__typ3] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp0,
        __tmp1,
        __tmp18: Optional[__typ2] = None,
        __tmp12: Optional[__typ2] = None,
        __tmp13: Optional[__typ2] = None,
        name: Optional[__typ2] = None,
        data: Optional[__typ3] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp14(__tmp0, __tmp1: __typ2) :
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp0, __tmp1) -> __typ3:
        raise NotImplementedError

    @abstractmethod
    def __tmp20(
        __tmp0,
        __tmp1: __typ2,
        __tmp4,
    ) -> Optional[Event]:
        raise NotImplementedError

    @abstractmethod
    def __tmp17(
        __tmp0,
        __tmp1: __typ2,
        __tmp9,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[Event]:
        raise NotImplementedError

    def __tmp6(
        __tmp0,
        __tmp1: __typ2,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ0:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp0, __tmp1: __typ2, __tmp2: Event) -> Event:
        raise NotImplementedError

    def insert_many(__tmp0, __tmp1, __tmp19: List[Event]) -> None:
        for __tmp2 in __tmp19:
            __tmp0.insert_one(__tmp1, __tmp2)

    @abstractmethod
    def __tmp7(__tmp0, __tmp1: __typ2, __tmp4: __typ0) -> __typ4:
        raise NotImplementedError

    @abstractmethod
    def __tmp16(__tmp0, __tmp1, __tmp4: __typ0, __tmp2) -> __typ4:
        raise NotImplementedError

    @abstractmethod
    def __tmp10(__tmp0, __tmp1, __tmp2: <FILL>) -> None:
        raise NotImplementedError
