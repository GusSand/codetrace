from typing import TypeAlias
__typ0 : TypeAlias = "int"
from abc import ABCMeta
from typing import List

from protoactor.сluster.member_status import MemberStatus


class __typ1():
    def __init__(__tmp1, statuses: List[MemberStatus]):
        if statuses is None:
            raise ValueError('statuses is empty')
        __tmp1._statuses = statuses

    @property
    def statuses(__tmp1) :
        return __tmp1._statuses


class AbstractMemberStatusEvent(metaclass=ABCMeta):
    def __init__(__tmp1, __tmp0: str, port: __typ0, kinds: List[str]):
        if __tmp0 is None:
            raise ValueError('host is none')
        __tmp1._host = __tmp0
        __tmp1._port = port

        if kinds is None:
            raise ValueError('kinds is none')
        __tmp1._kinds = kinds

    @property
    def address(__tmp1) :
        return __tmp1._host + ":" + str(__tmp1._port)

    @property
    def __tmp0(__tmp1) -> str:
        return __tmp1._host

    @property
    def port(__tmp1) :
        return __tmp1._port

    @property
    def kinds(__tmp1) :
        return __tmp1._kinds


class __typ4(AbstractMemberStatusEvent):
    def __init__(__tmp1, __tmp0: <FILL>, port, kinds):
        super().__init__(__tmp0, port, kinds)


class __typ3(AbstractMemberStatusEvent):
    def __init__(__tmp1, __tmp0, port: __typ0, kinds):
        super().__init__(__tmp0, port, kinds)


class __typ2(AbstractMemberStatusEvent):
    def __init__(__tmp1, __tmp0, port, kinds):
        super().__init__(__tmp0, port, kinds)
