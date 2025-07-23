from typing import TypeAlias
__typ1 : TypeAlias = "str"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ2(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(__tmp1, __tmp3) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp1, __tmp3, __tmp2, __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(__tmp1, __tmp3, inclusive_to_index) :
        raise NotImplementedError("Should Implement this method")


class __typ0(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(__tmp1, __tmp3: __typ1, index_start, index_end,
                         callback) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_event(__tmp1, __tmp3, __tmp2, event) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp1, __tmp3, inclusive_to_index: <FILL>) :
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(__typ0, __typ2, metaclass=ABCMeta):
    pass
