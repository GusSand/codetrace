from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "int"
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
    def __tmp8(__tmp0, testing) -> None:
        __tmp0.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp13(__tmp0) :
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        __tmp0,
        __tmp1,
        __tmp16,
        __tmp9,
        __tmp10,
        __tmp5,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp0,
        __tmp1,
        __tmp16: Optional[str] = None,
        __tmp9: Optional[str] = None,
        __tmp10: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp12(__tmp0, __tmp1) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp0, __tmp1) :
        raise NotImplementedError

    @abstractmethod
    def __tmp18(
        __tmp0,
        __tmp1,
        __tmp3,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp15(
        __tmp0,
        __tmp1,
        __tmp6: __typ1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        __tmp0,
        __tmp1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp0, __tmp1: <FILL>, __tmp2) :
        raise NotImplementedError

    def __tmp11(__tmp0, __tmp1, __tmp17) :
        for __tmp2 in __tmp17:
            __tmp0.insert_one(__tmp1, __tmp2)

    @abstractmethod
    def __tmp4(__tmp0, __tmp1, __tmp3) :
        raise NotImplementedError

    @abstractmethod
    def __tmp14(__tmp0, __tmp1, __tmp3, __tmp2) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def __tmp7(__tmp0, __tmp1, __tmp2: __typ0) :
        raise NotImplementedError
