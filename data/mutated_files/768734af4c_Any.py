from abc import abstractmethod
from typing import Iterable, Any, List

from protoactor.actor import PID


class __typ0:
    @abstractmethod
    def __tmp4(__tmp2) -> List[PID]:
        pass

    @abstractmethod
    def set_routees(__tmp2, __tmp3) -> None:
        pass

    @abstractmethod
    async def __tmp1(__tmp2, __tmp0: <FILL>) -> None:
        pass
