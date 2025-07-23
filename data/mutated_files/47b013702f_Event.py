from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event


class __typ2(metaclass=ABCMeta):
    """
    Interface for storage methods.
    """

    sid = "Storage id not set, fix me"

    @abstractmethod
    def __init__(self, testing: bool) -> None:
        self.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(self) -> Dict[__typ1, dict]:
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        self,
        __tmp0: __typ1,
        __tmp1: __typ1,
        client: __typ1,
        hostname: __typ1,
        created: __typ1,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        self,
        __tmp0,
        __tmp1: Optional[__typ1] = None,
        client: Optional[__typ1] = None,
        hostname: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(self, __tmp0: __typ1) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(self, __tmp0) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_event(
        self,
        __tmp0: __typ1,
        event_id,
    ) -> Optional[Event]:
        raise NotImplementedError

    @abstractmethod
    def get_events(
        self,
        __tmp0: __typ1,
        limit: __typ0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        self,
        __tmp0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ0:
        raise NotImplementedError

    @abstractmethod
    def insert_one(self, __tmp0, event: <FILL>) :
        raise NotImplementedError

    def insert_many(self, __tmp0, events) -> None:
        for event in events:
            self.insert_one(__tmp0, event)

    @abstractmethod
    def delete(self, __tmp0, event_id: __typ0) -> bool:
        raise NotImplementedError

    @abstractmethod
    def replace(self, __tmp0: __typ1, event_id: __typ0, event: Event) -> bool:
        raise NotImplementedError

    @abstractmethod
    def replace_last(self, __tmp0, event: Event) -> None:
        raise NotImplementedError
