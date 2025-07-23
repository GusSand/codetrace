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
    def __init__(__tmp1, testing: __typ3) -> None:
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
        client,
        hostname: str,
        created,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp1,
        __tmp0: str,
        type_id: Optional[str] = None,
        client: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ2] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp1, __tmp0: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp1, __tmp0: str) :
        raise NotImplementedError

    @abstractmethod
    def get_event(
        __tmp1,
        __tmp0,
        __tmp4: __typ0,
    ) -> Optional[__typ4]:
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp1,
        __tmp0: <FILL>,
        limit: __typ0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        __tmp1,
        __tmp0: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ0:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0, __tmp3) -> __typ4:
        raise NotImplementedError

    def insert_many(__tmp1, __tmp0: str, events: List[__typ4]) -> None:
        for __tmp3 in events:
            __tmp1.insert_one(__tmp0, __tmp3)

    @abstractmethod
    def delete(__tmp1, __tmp0: str, __tmp4: __typ0) :
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp1, __tmp0: str, __tmp4: __typ0, __tmp3) -> __typ3:
        raise NotImplementedError

    @abstractmethod
    def replace_last(__tmp1, __tmp0, __tmp3: __typ4) -> None:
        raise NotImplementedError
