from abc import ABCMeta
from typing import Optional, Any

from protoactor.actor.protos_pb2 import PID
from protoactor.actor.restart_statistics import RestartStatistics
from protoactor.actor.utils import Singleton


class __typ1():
    pass

class AbstractNotInfluenceReceiveTimeout(metaclass=ABCMeta):
    pass

class AutoReceiveMessage(metaclass=ABCMeta):
    pass


class Restarting(metaclass=Singleton):
    pass


class Restart(__typ1):
    def __tmp5(__tmp0, reason):
        __tmp0.reason = reason


class Failure(__typ1):
    def __tmp5(__tmp0, __tmp6, reason, __tmp1, message: Any) :
        __tmp0._who = __tmp6
        __tmp0._reason = reason
        __tmp0._crs = __tmp1
        __tmp0._message = message

    @property
    def __tmp6(__tmp0) :
        return __tmp0._who

    @property
    def reason(__tmp0) :
        return __tmp0._reason

    @property
    def restart_statistics(__tmp0) :
        return __tmp0._crs

    @property
    def message(__tmp0) :
        return __tmp0._message


class SystemMessage:
    pass


class Stopping(AutoReceiveMessage):
    pass


class Stopped(AutoReceiveMessage):
    pass


class Started(__typ1):
    pass


class ReceiveTimeout(__typ1, metaclass=Singleton):
    pass


class NotInfluenceReceiveTimeout(__typ1):
    pass


class PoisonPill(__typ1):
    pass


class Continuation(SystemMessage):
    def __tmp5(__tmp0, __tmp2, message):
        __tmp0.action = __tmp2
        __tmp0.message = message


class SuspendMailbox(SystemMessage):
    pass


class __typ0(SystemMessage):
    pass


class DeadLetterEvent:
    def __tmp5(__tmp0, __tmp4, message: <FILL>, __tmp3: Optional['PID']) :
        __tmp0._pid = __tmp4
        __tmp0._message = message
        __tmp0._sender = __tmp3

    @property
    def __tmp4(__tmp0) -> 'PID':
        return __tmp0._pid

    @property
    def message(__tmp0) :
        return __tmp0._message

    @property
    def __tmp3(__tmp0) :
        return __tmp0._sender
