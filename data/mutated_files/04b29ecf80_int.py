from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ2 : TypeAlias = "str"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp3(__tmp1, __tmp13) -> Tuple[__typ0, int]:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp10(__tmp1, __tmp13: __typ2, index: int, __tmp12: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp1, __tmp13, __tmp2) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp6(__tmp1, __tmp13: __typ2, __tmp8: int, __tmp7: <FILL>,
                         __tmp11) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp9(__tmp1, __tmp13: __typ2, index, __tmp4: __typ0) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp1, __tmp13: __typ2, __tmp2: int) :
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(__typ1, __typ3, metaclass=ABCMeta):
    pass
