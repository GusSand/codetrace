from typing import TypeAlias
__typ2 : TypeAlias = "dict"
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
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
    def __init__(__tmp1, testing) :
        __tmp1.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp1) :
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        __tmp1,
        __tmp0: str,
        type_id: str,
        __tmp3,
        hostname: str,
        created,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp1,
        __tmp0: str,
        type_id: Optional[str] = None,
        __tmp3: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp4(__tmp1, __tmp0) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp1, __tmp0: <FILL>) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def get_event(
        __tmp1,
        __tmp0,
        event_id: __typ1,
    ) :
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp1,
        __tmp0,
        limit,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ0]:
        raise NotImplementedError

    def get_eventcount(
        __tmp1,
        __tmp0: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0, event: __typ0) :
        raise NotImplementedError

    def insert_many(__tmp1, __tmp0: str, events: List[__typ0]) -> None:
        for event in events:
            __tmp1.insert_one(__tmp0, event)

    @abstractmethod
    def __tmp5(__tmp1, __tmp0: str, event_id: __typ1) :
        raise NotImplementedError

    @abstractmethod
    def replace(__tmp1, __tmp0: str, event_id: __typ1, event) :
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp1, __tmp0: str, event) -> None:
        raise NotImplementedError
