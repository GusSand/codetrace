from typing import TypeAlias
__typ1 : TypeAlias = "AbstractMemberStatusValue"
__typ2 : TypeAlias = "AbstractMemberStatusValueSerializer"
from abc import ABCMeta, abstractmethod
from typing import List

from protoactor.cluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer


class __typ0(metaclass=ABCMeta):
    @abstractmethod
    async def register_member_async(__tmp2, cluster_name: str, host: <FILL>, port: int, kinds: List[str],
                                    __tmp3: __typ1,
                                    __tmp1) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def monitor_member_status_changes(__tmp2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def update_member_status_value_async(__tmp2, __tmp3: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp2) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def shutdown(__tmp2) -> None:
        raise NotImplementedError("Should Implement this method")
