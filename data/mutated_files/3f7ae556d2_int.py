from typing import TypeAlias
__typ2 : TypeAlias = "AbstractMemberStatusValue"
__typ3 : TypeAlias = "AbstractMemberStatusValueSerializer"
__typ1 : TypeAlias = "str"
from abc import ABCMeta, abstractmethod
from typing import List

from protoactor.сluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer


class __typ0(metaclass=ABCMeta):
    @abstractmethod
    async def register_member_async(__tmp2, cluster_name, host, port: <FILL>, kinds,
                                    __tmp5,
                                    __tmp3: __typ3) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def monitor_member_status_changes(__tmp2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp1(__tmp2, __tmp5) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp4(__tmp2) -> None:
        raise NotImplementedError("Should Implement this method")
