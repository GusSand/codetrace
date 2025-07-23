from typing import TypeAlias
__typ2 : TypeAlias = "object"
from abc import ABCMeta
from typing import Optional, Any

from protoactor.actor.protos_pb2 import PID
from protoactor.actor.restart_statistics import RestartStatistics
from protoactor.actor.utils import Singleton


class __typ3():
    pass

class AbstractNotInfluenceReceiveTimeout(metaclass=ABCMeta):
    pass

class AutoReceiveMessage(metaclass=ABCMeta):
    pass


class Restarting(metaclass=Singleton):
    pass


class Restart(__typ3):
    def __tmp2(__tmp1, reason):
        __tmp1.reason = reason


class Failure(__typ3):
    def __tmp2(__tmp1, __tmp0: <FILL>, reason: Exception, crs, message: Any) -> None:
        __tmp1._who = __tmp0
        __tmp1._reason = reason
        __tmp1._crs = crs
        __tmp1._message = message

    @property
    def __tmp0(__tmp1) :
        return __tmp1._who

    @property
    def reason(__tmp1) -> Exception:
        return __tmp1._reason

    @property
    def restart_statistics(__tmp1) :
        return __tmp1._crs

    @property
    def message(__tmp1) :
        return __tmp1._message


class __typ5:
    pass


class __typ0(AutoReceiveMessage):
    pass


class Stopped(AutoReceiveMessage):
    pass


class Started(__typ3):
    pass


class ReceiveTimeout(__typ3, metaclass=Singleton):
    pass


class __typ1(__typ3):
    pass


class PoisonPill(__typ3):
    pass


class Continuation(__typ5):
    def __tmp2(__tmp1, fun, message):
        __tmp1.action = fun
        __tmp1.message = message


class SuspendMailbox(__typ5):
    pass


class ResumeMailbox(__typ5):
    pass


class __typ4:
    def __tmp2(__tmp1, pid: 'PID', message: __typ2, __tmp3: Optional['PID']) :
        __tmp1._pid = pid
        __tmp1._message = message
        __tmp1._sender = __tmp3

    @property
    def pid(__tmp1) -> 'PID':
        return __tmp1._pid

    @property
    def message(__tmp1) :
        return __tmp1._message

    @property
    def __tmp3(__tmp1) :
        return __tmp1._sender
