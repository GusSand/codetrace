from abc import abstractmethod, ABCMeta
import queue
from typing import Optional


class AbstractQueue(metaclass=ABCMeta):
    @abstractmethod
    def __tmp1(__tmp0) -> bool:
        raise NotImplementedError("Should Implement this method.")

    @abstractmethod
    def push(__tmp0, message: <FILL>):
        raise NotImplementedError("Should Implement this method.")

    @abstractmethod
    def __tmp2(__tmp0) :
        raise NotImplementedError("Should Implement this method.")


class UnboundedMailboxQueue(AbstractQueue):
    def __init__(__tmp0):
        __tmp0._messages = queue.Queue()

    def __tmp2(__tmp0) :
        try:
            return __tmp0._messages.get_nowait()
        except queue.Empty:
            return None

    def push(__tmp0, message: object):
        __tmp0._messages.put_nowait(message)

    def __tmp1(__tmp0) :
        return not __tmp0._messages.empty()
