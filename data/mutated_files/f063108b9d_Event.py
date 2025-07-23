from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
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
    def __tmp12(__tmp0, testing) :
        __tmp0.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
        __tmp0,
        __tmp1,
        __tmp18,
        __tmp13,
        __tmp14,
        __tmp9,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp0,
        __tmp1: __typ1,
        __tmp18: Optional[__typ1] = None,
        __tmp13: Optional[__typ1] = None,
        __tmp14: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp0, __tmp1) :
        raise NotImplementedError

    @abstractmethod
    def __tmp6(__tmp0, __tmp1) :
        raise NotImplementedError

    @abstractmethod
    def __tmp19(
        __tmp0,
        __tmp1,
        __tmp4,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp17(
        __tmp0,
        __tmp1,
        __tmp10,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def __tmp7(
        __tmp0,
        __tmp1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp0, __tmp1, __tmp2) :
        raise NotImplementedError

    def __tmp15(__tmp0, __tmp1, events) :
        for __tmp2 in events:
            __tmp0.insert_one(__tmp1, __tmp2)

    @abstractmethod
    def __tmp8(__tmp0, __tmp1, __tmp4) :
        raise NotImplementedError

    @abstractmethod
    def __tmp16(__tmp0, __tmp1, __tmp4, __tmp2: <FILL>) :
        raise NotImplementedError

    @abstractmethod
    def __tmp11(__tmp0, __tmp1, __tmp2: Event) -> None:
        raise NotImplementedError
