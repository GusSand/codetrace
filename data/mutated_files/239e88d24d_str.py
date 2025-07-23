from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(__tmp1, __tmp8) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp1, __tmp8: <FILL>, index, snapshot) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(__tmp1, __tmp8, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")


class AbstractEventStore(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp1, __tmp8, __tmp6: int, __tmp2,
                         callback) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp1, __tmp8, index, __tmp3) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp4(__tmp1, __tmp8, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class __typ0(AbstractEventStore, __typ1, metaclass=ABCMeta):
    pass
