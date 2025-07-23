from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "dict"
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
    def __tmp7(__tmp1, testing: __typ2) -> None:
        __tmp1.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp1) -> Dict[str, __typ1]:
        raise NotImplementedError

    @abstractmethod
    def __tmp4(
        __tmp1,
        __tmp0,
        type_id: str,
        client: str,
        hostname: str,
        __tmp9: <FILL>,
        name: Optional[str] = None,
        data: Optional[__typ1] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp1,
        __tmp0: str,
        type_id: Optional[str] = None,
        client: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[__typ1] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp1, __tmp0) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp1, __tmp0: str) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def get_event(
        __tmp1,
        __tmp0: str,
        __tmp5: int,
    ) -> Optional[__typ0]:
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp1,
        __tmp0,
        __tmp3: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ0]:
        raise NotImplementedError

    def get_eventcount(
        __tmp1,
        __tmp0: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0: str, __tmp2: __typ0) -> __typ0:
        raise NotImplementedError

    def insert_many(__tmp1, __tmp0, events: List[__typ0]) -> None:
        for __tmp2 in events:
            __tmp1.insert_one(__tmp0, __tmp2)

    @abstractmethod
    def __tmp8(__tmp1, __tmp0, __tmp5: int) :
        raise NotImplementedError

    @abstractmethod
    def replace(__tmp1, __tmp0: str, __tmp5: int, __tmp2: __typ0) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def __tmp6(__tmp1, __tmp0: str, __tmp2: __typ0) -> None:
        raise NotImplementedError
