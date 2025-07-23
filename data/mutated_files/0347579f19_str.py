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
    def __init__(__tmp1, testing) :
        __tmp1.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp1) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
        __tmp1,
        __tmp0: str,
        type_id,
        __tmp5,
        hostname,
        created,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp1,
        __tmp0,
        type_id: Optional[str] = None,
        __tmp5: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp1, __tmp0: str) :
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp1, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp6(
        __tmp1,
        __tmp0: <FILL>,
        event_id: __typ0,
    ) :
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp1,
        __tmp0: str,
        limit,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        __tmp1,
        __tmp0: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0, __tmp2: __typ4) -> __typ4:
        raise NotImplementedError

    def insert_many(__tmp1, __tmp0, events) :
        for __tmp2 in events:
            __tmp1.insert_one(__tmp0, __tmp2)

    @abstractmethod
    def delete(__tmp1, __tmp0, event_id) :
        raise NotImplementedError

    @abstractmethod
    def replace(__tmp1, __tmp0, event_id, __tmp2) :
        raise NotImplementedError

    @abstractmethod
    def __tmp4(__tmp1, __tmp0: str, __tmp2: __typ4) :
        raise NotImplementedError
