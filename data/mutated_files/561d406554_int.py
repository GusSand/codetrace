from typing import TypeAlias
__typ3 : TypeAlias = "AbstractMemberStatusValue"
__typ0 : TypeAlias = "AbstractMemberStatusValueSerializer"
__typ1 : TypeAlias = "str"
from abc import ABCMeta, abstractmethod
from typing import List

from protoactor.cluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer


class __typ2(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp1(__tmp2, __tmp3: __typ1, __tmp5, port: <FILL>, kinds: List[__typ1],
                                    __tmp6: __typ3,
                                    __tmp4) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def monitor_member_status_changes(__tmp2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def update_member_status_value_async(__tmp2, __tmp6) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def shutdown(__tmp2) -> None:
        raise NotImplementedError("Should Implement this method")
