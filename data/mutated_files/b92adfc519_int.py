from typing import TypeAlias
__typ2 : TypeAlias = "bool"
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
    def __init__(__tmp1, testing) -> None:
        __tmp1.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp1) -> Dict[__typ1, dict]:
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        __tmp1,
        __tmp0: __typ1,
        type_id,
        client: __typ1,
        __tmp6: __typ1,
        created: __typ1,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp1,
        __tmp0: __typ1,
        type_id: Optional[__typ1] = None,
        client: Optional[__typ1] = None,
        __tmp6: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp4(__tmp1, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp1, __tmp0: __typ1) -> dict:
        raise NotImplementedError

    @abstractmethod
    def __tmp8(
        __tmp1,
        __tmp0,
        event_id: int,
    ) -> Optional[__typ0]:
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp1,
        __tmp0: __typ1,
        limit: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ0]:
        raise NotImplementedError

    def get_eventcount(
        __tmp1,
        __tmp0: __typ1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0: __typ1, __tmp3: __typ0) -> __typ0:
        raise NotImplementedError

    def insert_many(__tmp1, __tmp0: __typ1, __tmp7: List[__typ0]) -> None:
        for __tmp3 in __tmp7:
            __tmp1.insert_one(__tmp0, __tmp3)

    @abstractmethod
    def delete(__tmp1, __tmp0: __typ1, event_id: <FILL>) :
        raise NotImplementedError

    @abstractmethod
    def __tmp2(__tmp1, __tmp0: __typ1, event_id: int, __tmp3: __typ0) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def __tmp5(__tmp1, __tmp0, __tmp3) -> None:
        raise NotImplementedError
