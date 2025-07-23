from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ2 : TypeAlias = "str"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class AbstractSnapshotStore(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp1(__tmp0, __tmp13) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp11(__tmp0, __tmp13, __tmp14, __tmp12) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp3(__tmp0, __tmp13, __tmp2) :
        raise NotImplementedError("Should Implement this method")


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp0, __tmp13, __tmp8: <FILL>, __tmp7,
                         __tmp10) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp9(__tmp0, __tmp13, __tmp14, __tmp4) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp0, __tmp13, __tmp2) :
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(__typ1, AbstractSnapshotStore, metaclass=ABCMeta):
    pass
