from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "int"
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event


class __typ3(metaclass=ABCMeta):
    """
    Interface for storage methods.
    """

    sid = "Storage id not set, fix me"

    @abstractmethod
    def __tmp7(__tmp2, testing) :
        __tmp2.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp1(__tmp2) :
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp2,
        __tmp0,
        __tmp6,
        client,
        __tmp8,
        created,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp2,
        __tmp0: str,
        __tmp6: Optional[str] = None,
        client: Optional[str] = None,
        __tmp8: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp2, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp2, __tmp0) :
        raise NotImplementedError

    @abstractmethod
    def get_event(
        __tmp2,
        __tmp0,
        event_id,
    ) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(
        __tmp2,
        __tmp0: str,
        __tmp4,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        __tmp2,
        __tmp0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp2, __tmp0, event) :
        raise NotImplementedError

    def __tmp9(__tmp2, __tmp0, events) :
        for event in events:
            __tmp2.insert_one(__tmp0, event)

    @abstractmethod
    def delete(__tmp2, __tmp0, event_id) :
        raise NotImplementedError

    @abstractmethod
    def replace(__tmp2, __tmp0, event_id, event) :
        raise NotImplementedError

    @abstractmethod
    def replace_last(__tmp2, __tmp0: <FILL>, event) :
        raise NotImplementedError
