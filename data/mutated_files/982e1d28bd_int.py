from typing import TypeAlias
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "str"
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event


class AbstractStorage(metaclass=ABCMeta):
    """
    Interface for storage methods.
    """

    sid = "Storage id not set, fix me"

    @abstractmethod
    def __tmp11(__tmp0, testing) :
        __tmp0.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp15(__tmp0) -> Dict[__typ1, dict]:
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
        __tmp0,
        __tmp1,
        __tmp18,
        __tmp12: __typ1,
        __tmp13,
        __tmp9: __typ1,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp0,
        __tmp1: __typ1,
        __tmp18: Optional[__typ1] = None,
        __tmp12: Optional[__typ1] = None,
        __tmp13: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp14(__tmp0, __tmp1: __typ1) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp6(__tmp0, __tmp1: __typ1) :
        raise NotImplementedError

    @abstractmethod
    def __tmp20(
        __tmp0,
        __tmp1: __typ1,
        __tmp4: int,
    ) -> Optional[__typ0]:
        raise NotImplementedError

    @abstractmethod
    def __tmp17(
        __tmp0,
        __tmp1: __typ1,
        limit: <FILL>,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def __tmp7(
        __tmp0,
        __tmp1: __typ1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp0, __tmp1, __tmp2: __typ0) -> __typ0:
        raise NotImplementedError

    def insert_many(__tmp0, __tmp1: __typ1, __tmp19: List[__typ0]) -> None:
        for __tmp2 in __tmp19:
            __tmp0.insert_one(__tmp1, __tmp2)

    @abstractmethod
    def __tmp8(__tmp0, __tmp1: __typ1, __tmp4: int) :
        raise NotImplementedError

    @abstractmethod
    def __tmp16(__tmp0, __tmp1: __typ1, __tmp4: int, __tmp2: __typ0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp10(__tmp0, __tmp1: __typ1, __tmp2: __typ0) -> None:
        raise NotImplementedError
