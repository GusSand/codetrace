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
    def __tmp11(__tmp1, testing) -> None:
        __tmp1.testing = True
        raise NotImplementedError

    @abstractmethod
    def buckets(__tmp1) -> Dict[str, dict]:
        raise NotImplementedError

    @abstractmethod
    def __tmp6(
        __tmp1,
        __tmp0: str,
        __tmp8: str,
        __tmp13: str,
        __tmp14: <FILL>,
        created: str,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp12(
        __tmp1,
        __tmp0: str,
        __tmp8: Optional[str] = None,
        __tmp13: Optional[str] = None,
        __tmp14: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def __tmp5(__tmp1, __tmp0: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp1, __tmp0: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def __tmp17(
        __tmp1,
        __tmp0: str,
        __tmp9,
    ) -> Optional[__typ0]:
        raise NotImplementedError

    @abstractmethod
    def __tmp4(
        __tmp1,
        __tmp0: str,
        limit: __typ1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ0]:
        raise NotImplementedError

    def __tmp16(
        __tmp1,
        __tmp0: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ1:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp1, __tmp0: str, __tmp3: __typ0) -> __typ0:
        raise NotImplementedError

    def __tmp2(__tmp1, __tmp0, __tmp15: List[__typ0]) -> None:
        for __tmp3 in __tmp15:
            __tmp1.insert_one(__tmp0, __tmp3)

    @abstractmethod
    def __tmp7(__tmp1, __tmp0, __tmp9: __typ1) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def replace(__tmp1, __tmp0: str, __tmp9, __tmp3: __typ0) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def __tmp10(__tmp1, __tmp0: str, __tmp3: __typ0) -> None:
        raise NotImplementedError
