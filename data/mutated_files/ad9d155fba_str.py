from typing import TypeAlias
__typ2 : TypeAlias = "AbstractMemberStatusValue"
__typ3 : TypeAlias = "AbstractMemberStatusValueSerializer"
__typ1 : TypeAlias = "int"
from abc import ABCMeta, abstractmethod
from typing import List

from protoactor.сluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer


class __typ0(metaclass=ABCMeta):
    @abstractmethod
    async def register_member_async(__tmp1, cluster_name, __tmp3: <FILL>, port, kinds,
                                    __tmp5,
                                    __tmp2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp4(__tmp1) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def update_member_status_value_async(__tmp1, __tmp5) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp1) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def shutdown(__tmp1) :
        raise NotImplementedError("Should Implement this method")
