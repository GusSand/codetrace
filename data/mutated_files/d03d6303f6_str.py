from typing import TypeAlias
__typ0 : TypeAlias = "dict"
__typ1 : TypeAlias = "bool"
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
    def __tmp12(__tmp2, testing: __typ1) -> None:
        __tmp2.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp1(__tmp2) :
        raise NotImplementedError

    @abstractmethod
    def __tmp7(
        __tmp2,
        __tmp0,
        __tmp9,
        __tmp13,
        __tmp14,
        created,
        name: Optional[str] = None,
        data: Optional[__typ0] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp2,
        __tmp0: str,
        __tmp9: Optional[str] = None,
        __tmp13: Optional[str] = None,
        __tmp14: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ0] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp2, __tmp0: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp2, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp16(
        __tmp2,
        __tmp0,
        __tmp10: int,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp2,
        __tmp0,
        __tmp6: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        __tmp2,
        __tmp0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp2, __tmp0, __tmp4: Event) :
        raise NotImplementedError

    def __tmp15(__tmp2, __tmp0, events: List[Event]) :
        for __tmp4 in events:
            __tmp2.insert_one(__tmp0, __tmp4)

    @abstractmethod
    def __tmp8(__tmp2, __tmp0, __tmp10) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(__tmp2, __tmp0: <FILL>, __tmp10: int, __tmp4) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def __tmp11(__tmp2, __tmp0: str, __tmp4: Event) -> None:
        raise NotImplementedError
