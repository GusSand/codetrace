from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ2(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(self, actor_name: __typ0) -> Tuple[any, __typ1]:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp1(self, actor_name: __typ0, index, snapshot) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(self, actor_name: __typ0, __tmp0: __typ1) :
        raise NotImplementedError("Should Implement this method")


class AbstractEventStore(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(self, actor_name: __typ0, index_start: __typ1, index_end: __typ1,
                         callback) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_event(self, actor_name, index: __typ1, event: <FILL>) -> __typ1:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(self, actor_name: __typ0, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(AbstractEventStore, __typ2, metaclass=ABCMeta):
    pass
