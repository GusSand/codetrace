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
    def __tmp11(__tmp1, testing: __typ2) :
        __tmp1.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp1) :
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        __tmp1,
        __tmp0: <FILL>,
        __tmp8,
        client,
        __tmp13,
        __tmp17,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp12(
        __tmp1,
        __tmp0,
        __tmp8: Optional[str] = None,
        client: Optional[str] = None,
        __tmp13: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp5(__tmp1, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp7(__tmp1, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp16(
        __tmp1,
        __tmp0: str,
        __tmp9,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp4(
        __tmp1,
        __tmp0,
        __tmp6,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def __tmp15(
        __tmp1,
        __tmp0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0, __tmp3) :
        raise NotImplementedError

    def __tmp2(__tmp1, __tmp0, __tmp14) -> None:
        for __tmp3 in __tmp14:
            __tmp1.insert_one(__tmp0, __tmp3)

    @abstractmethod
    def delete(__tmp1, __tmp0, __tmp9) :
        raise NotImplementedError

    @abstractmethod
    def replace(__tmp1, __tmp0, __tmp9: __typ1, __tmp3) :
        raise NotImplementedError

    @abstractmethod
    def __tmp10(__tmp1, __tmp0, __tmp3: __typ0) :
        raise NotImplementedError
