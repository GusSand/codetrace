from typing import TypeAlias
__typ3 : TypeAlias = "RestartStatistics"
__typ2 : TypeAlias = "PID"
__typ5 : TypeAlias = "Exception"
from abc import ABCMeta
from typing import Optional, Any

from protoactor.actor.protos_pb2 import PID
from protoactor.actor.restart_statistics import RestartStatistics
from protoactor.actor.utils import Singleton


class AbstractSystemMessage():
    pass

class __typ4(metaclass=ABCMeta):
    pass

class __typ6(metaclass=ABCMeta):
    pass


class Restarting(metaclass=Singleton):
    pass


class Restart(AbstractSystemMessage):
    def __tmp5(__tmp0, reason):
        __tmp0.reason = reason


class Failure(AbstractSystemMessage):
    def __tmp5(__tmp0, __tmp6: __typ2, reason: __typ5, __tmp1, message: <FILL>) -> None:
        __tmp0._who = __tmp6
        __tmp0._reason = reason
        __tmp0._crs = __tmp1
        __tmp0._message = message

    @property
    def __tmp6(__tmp0) -> __typ2:
        return __tmp0._who

    @property
    def reason(__tmp0) -> __typ5:
        return __tmp0._reason

    @property
    def restart_statistics(__tmp0) -> __typ3:
        return __tmp0._crs

    @property
    def message(__tmp0) -> Any:
        return __tmp0._message


class __typ8:
    pass


class __typ0(__typ6):
    pass


class Stopped(__typ6):
    pass


class __typ7(AbstractSystemMessage):
    pass


class ReceiveTimeout(AbstractSystemMessage, metaclass=Singleton):
    pass


class __typ1(AbstractSystemMessage):
    pass


class PoisonPill(AbstractSystemMessage):
    pass


class Continuation(__typ8):
    def __tmp5(__tmp0, __tmp2, message):
        __tmp0.action = __tmp2
        __tmp0.message = message


class SuspendMailbox(__typ8):
    pass


class ResumeMailbox(__typ8):
    pass


class DeadLetterEvent:
    def __tmp5(__tmp0, __tmp4: 'PID', message: object, __tmp3: Optional['PID']) -> None:
        __tmp0._pid = __tmp4
        __tmp0._message = message
        __tmp0._sender = __tmp3

    @property
    def __tmp4(__tmp0) -> 'PID':
        return __tmp0._pid

    @property
    def message(__tmp0) -> object:
        return __tmp0._message

    @property
    def __tmp3(__tmp0) -> Optional['PID']:
        return __tmp0._sender
