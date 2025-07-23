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
    def __init__(__tmp2, testing: __typ3) :
        __tmp2.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp1(__tmp2) :
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        __tmp2,
        __tmp0,
        __tmp6,
        client: str,
        __tmp9,
        __tmp12: str,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp2,
        __tmp0,
        __tmp6: Optional[str] = None,
        client: Optional[str] = None,
        __tmp9: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp10(__tmp2, __tmp0: <FILL>) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp2, __tmp0: str) :
        raise NotImplementedError

    @abstractmethod
    def get_event(
        __tmp2,
        __tmp0,
        __tmp7: __typ0,
    ) :
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp2,
        __tmp0,
        limit: __typ0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def __tmp11(
        __tmp2,
        __tmp0: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp2, __tmp0, __tmp5) :
        raise NotImplementedError

    def __tmp4(__tmp2, __tmp0, events) :
        for __tmp5 in events:
            __tmp2.insert_one(__tmp0, __tmp5)

    @abstractmethod
    def delete(__tmp2, __tmp0: str, __tmp7) -> __typ3:
        raise NotImplementedError

    @abstractmethod
    def __tmp3(__tmp2, __tmp0, __tmp7, __tmp5) :
        raise NotImplementedError

    @abstractmethod
    def __tmp8(__tmp2, __tmp0, __tmp5) :
        raise NotImplementedError
