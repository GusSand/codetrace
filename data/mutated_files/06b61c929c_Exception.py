from typing import TypeAlias
__typ3 : TypeAlias = "Restart"
__typ1 : TypeAlias = "RestartStatistics"
__typ6 : TypeAlias = "PID"
__typ8 : TypeAlias = "object"
__typ7 : TypeAlias = "Any"
from abc import ABCMeta
from typing import Optional, Any

from protoactor.actor.protos_pb2 import PID
from protoactor.actor.restart_statistics import RestartStatistics
from protoactor.actor.utils import Singleton


class __typ9():
    pass

class __typ15(metaclass=ABCMeta):
    pass

class __typ17(metaclass=ABCMeta):
    pass


class __typ18(metaclass=Singleton):
    pass


class __typ3(__typ9):
    def __tmp3(__tmp0, reason):
        __tmp0.reason = reason


class __typ14(__typ9):
    def __tmp3(__tmp0, __tmp4: __typ6, reason: <FILL>, crs: __typ1, message: __typ7) -> None:
        __tmp0._who = __tmp4
        __tmp0._reason = reason
        __tmp0._crs = crs
        __tmp0._message = message

    @property
    def __tmp4(__tmp0) :
        return __tmp0._who

    @property
    def reason(__tmp0) :
        return __tmp0._reason

    @property
    def restart_statistics(__tmp0) -> __typ1:
        return __tmp0._crs

    @property
    def message(__tmp0) -> __typ7:
        return __tmp0._message


class __typ5:
    pass


class __typ12(__typ17):
    pass


class Stopped(__typ17):
    pass


class Started(__typ9):
    pass


class __typ10(__typ9, metaclass=Singleton):
    pass


class __typ13(__typ9):
    pass


class __typ0(__typ9):
    pass


class __typ2(__typ5):
    def __tmp3(__tmp0, fun, message):
        __tmp0.action = fun
        __tmp0.message = message


class __typ11(__typ5):
    pass


class __typ16(__typ5):
    pass


class __typ4:
    def __tmp3(__tmp0, __tmp2: 'PID', message: __typ8, __tmp1: Optional['PID']) -> None:
        __tmp0._pid = __tmp2
        __tmp0._message = message
        __tmp0._sender = __tmp1

    @property
    def __tmp2(__tmp0) -> 'PID':
        return __tmp0._pid

    @property
    def message(__tmp0) :
        return __tmp0._message

    @property
    def __tmp1(__tmp0) -> Optional['PID']:
        return __tmp0._sender
