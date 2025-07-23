from abc import ABCMeta, abstractmethod
from typing import List

from protoactor.cluster.member_status import AbstractMemberStatusValue, AbstractMemberStatusValueSerializer


class AbstractClusterProvider(metaclass=ABCMeta):
    @abstractmethod
    async def register_member_async(__tmp3, cluster_name: <FILL>, __tmp1, port, kinds,
                                    status_value: AbstractMemberStatusValue,
                                    __tmp2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def monitor_member_status_changes(__tmp3) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp3, status_value: AbstractMemberStatusValue) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def deregister_member_async(__tmp3) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def shutdown(__tmp3) :
        raise NotImplementedError("Should Implement this method")
