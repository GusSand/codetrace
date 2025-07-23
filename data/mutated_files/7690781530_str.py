from typing import TypeAlias
__typ2 : TypeAlias = "AbstractMemberStatusValue"
__typ1 : TypeAlias = "int"
from abc import ABCMeta, abstractmethod
from typing import List

from protoactor.сluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer


class __typ0(metaclass=ABCMeta):
    @abstractmethod
    async def register_member_async(self, cluster_name: <FILL>, host: str, port, __tmp0: List[str],
                                    __tmp1,
                                    serializer: AbstractMemberStatusValueSerializer) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def monitor_member_status_changes(self) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def update_member_status_value_async(self, __tmp1: __typ2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def deregister_member_async(self) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError("Should Implement this method")
