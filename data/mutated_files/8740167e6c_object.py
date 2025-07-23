from abc import abstractmethod, ABCMeta
import queue
from typing import Optional


class AbstractQueue(metaclass=ABCMeta):
    @abstractmethod
    def __tmp2(__tmp1) :
        raise NotImplementedError("Should Implement this method.")

    @abstractmethod
    def __tmp4(__tmp1, __tmp0):
        raise NotImplementedError("Should Implement this method.")

    @abstractmethod
    def __tmp5(__tmp1) -> Optional[object]:
        raise NotImplementedError("Should Implement this method.")


class __typ0(AbstractQueue):
    def __tmp3(__tmp1):
        __tmp1._messages = queue.Queue()

    def __tmp5(__tmp1) -> Optional[object]:
        try:
            return __tmp1._messages.get_nowait()
        except queue.Empty:
            return None

    def __tmp4(__tmp1, __tmp0: <FILL>):
        __tmp1._messages.put_nowait(__tmp0)

    def __tmp2(__tmp1) :
        return not __tmp1._messages.empty()
