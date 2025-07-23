from typing import TypeAlias
__typ4 : TypeAlias = "Event"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "dict"
__typ0 : TypeAlias = "int"
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
    def __tmp5(__tmp2, testing: <FILL>) :
        __tmp2.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp2) :
        raise NotImplementedError

    @abstractmethod
    def create_bucket(
        __tmp2,
        __tmp0,
        type_id: __typ2,
        client: __typ2,
        hostname: __typ2,
        __tmp7: __typ2,
        name: Optional[__typ2] = None,
        data: Optional[__typ3] = None,
    ) :
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp2,
        __tmp0,
        type_id: Optional[__typ2] = None,
        client: Optional[__typ2] = None,
        hostname: Optional[__typ2] = None,
        name: Optional[__typ2] = None,
        data: Optional[__typ3] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp2, __tmp0: __typ2) :
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp2, __tmp0: __typ2) :
        raise NotImplementedError

    @abstractmethod
    def __tmp1(
        __tmp2,
        __tmp0,
        __tmp4,
    ) :
        raise NotImplementedError

    @abstractmethod
    def get_events(
        __tmp2,
        __tmp0: __typ2,
        limit,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def get_eventcount(
        __tmp2,
        __tmp0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ0:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp2, __tmp0, event: __typ4) -> __typ4:
        raise NotImplementedError

    def insert_many(__tmp2, __tmp0, events) :
        for event in events:
            __tmp2.insert_one(__tmp0, event)

    @abstractmethod
    def __tmp6(__tmp2, __tmp0: __typ2, __tmp4) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(__tmp2, __tmp0, __tmp4, event: __typ4) :
        raise NotImplementedError

    @abstractmethod
    def replace_last(__tmp2, __tmp0, event: __typ4) -> None:
        raise NotImplementedError
