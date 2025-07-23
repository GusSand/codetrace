from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp2(__tmp3, __tmp8) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp3, __tmp8: __typ2, index: __typ0, __tmp9: <FILL>) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp3, __tmp8, __tmp1) :
        raise NotImplementedError("Should Implement this method")


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp3, __tmp8, index_start: __typ0, index_end,
                         __tmp7) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp3, __tmp8, index, event) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp4(__tmp3, __tmp8, __tmp1) :
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(__typ1, __typ3, metaclass=ABCMeta):
    pass
