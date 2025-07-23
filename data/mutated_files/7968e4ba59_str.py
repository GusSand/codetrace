from typing import TypeAlias
__typ1 : TypeAlias = "int"
from abc import ABCMeta
from typing import List

from protoactor.cluster.member_status import MemberStatus


class __typ0():
    def __init__(__tmp1, statuses):
        if statuses is None:
            raise ValueError('statuses is empty')
        __tmp1._statuses = statuses

    @property
    def statuses(__tmp1) -> List[MemberStatus]:
        return __tmp1._statuses


class __typ3(metaclass=ABCMeta):
    def __init__(__tmp1, host: str, port: __typ1, __tmp0):
        if host is None:
            raise ValueError('host is none')
        __tmp1._host = host
        __tmp1._port = port

        if __tmp0 is None:
            raise ValueError('kinds is none')
        __tmp1._kinds = __tmp0

    @property
    def address(__tmp1) :
        return __tmp1._host + ":" + str(__tmp1._port)

    @property
    def host(__tmp1) :
        return __tmp1._host

    @property
    def port(__tmp1) -> __typ1:
        return __tmp1._port

    @property
    def __tmp0(__tmp1) -> List[str]:
        return __tmp1._kinds


class MemberJoinedEvent(__typ3):
    def __init__(__tmp1, host, port: __typ1, __tmp0):
        super().__init__(host, port, __tmp0)


class __typ2(__typ3):
    def __init__(__tmp1, host: <FILL>, port, __tmp0: List[str]):
        super().__init__(host, port, __tmp0)


class MemberLeftEvent(__typ3):
    def __init__(__tmp1, host: str, port, __tmp0: List[str]):
        super().__init__(host, port, __tmp0)
