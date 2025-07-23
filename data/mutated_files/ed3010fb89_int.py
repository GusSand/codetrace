from typing import TypeAlias
__typ2 : TypeAlias = "dict"
__typ4 : TypeAlias = "Event"
__typ3 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event


class __typ0(metaclass=ABCMeta):
    """
    Interface for storage methods.
    """

    sid = "Storage id not set, fix me"

    @abstractmethod
    def __tmp9(__tmp2, testing: __typ3) -> None:
        __tmp2.testing = True
        raise NotImplementedError

    @abstractmethod
    def __tmp1(__tmp2) -> Dict[__typ1, __typ2]:
        raise NotImplementedError

    @abstractmethod
    def __tmp6(
        __tmp2,
        __tmp0: __typ1,
        __tmp7: __typ1,
        client: __typ1,
        __tmp10: __typ1,
        created: __typ1,
        name: Optional[__typ1] = None,
        data: Optional[__typ2] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_bucket(
        __tmp2,
        __tmp0: __typ1,
        __tmp7: Optional[__typ1] = None,
        client: Optional[__typ1] = None,
        __tmp10: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        data: Optional[__typ2] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_bucket(__tmp2, __tmp0: __typ1) :
        raise NotImplementedError

    @abstractmethod
    def get_metadata(__tmp2, __tmp0: __typ1) -> __typ2:
        raise NotImplementedError

    @abstractmethod
    def __tmp13(
        __tmp2,
        __tmp0: __typ1,
        __tmp8: <FILL>,
    ) -> Optional[__typ4]:
        raise NotImplementedError

    @abstractmethod
    def __tmp5(
        __tmp2,
        __tmp0: __typ1,
        limit: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        raise NotImplementedError

    def __tmp12(
        __tmp2,
        __tmp0: __typ1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def insert_one(__tmp2, __tmp0: __typ1, __tmp4) -> __typ4:
        raise NotImplementedError

    def insert_many(__tmp2, __tmp0, __tmp11: List[__typ4]) -> None:
        for __tmp4 in __tmp11:
            __tmp2.insert_one(__tmp0, __tmp4)

    @abstractmethod
    def delete(__tmp2, __tmp0: __typ1, __tmp8) :
        raise NotImplementedError

    @abstractmethod
    def __tmp3(__tmp2, __tmp0: __typ1, __tmp8: int, __tmp4: __typ4) -> __typ3:
        raise NotImplementedError

    @abstractmethod
    def replace_last(__tmp2, __tmp0: __typ1, __tmp4) -> None:
        raise NotImplementedError
