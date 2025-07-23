from typing import TypeAlias
__typ1 : TypeAlias = "str"
from abc import ABCMeta
from typing import List

from protoactor.сluster.member_status import MemberStatus


class __typ0():
    def __init__(__tmp1, statuses):
        if statuses is None:
            raise ValueError('statuses is empty')
        __tmp1._statuses = statuses

    @property
    def statuses(__tmp1) -> List[MemberStatus]:
        return __tmp1._statuses


class __typ3(metaclass=ABCMeta):
    def __init__(__tmp1, __tmp0, port, kinds):
        if __tmp0 is None:
            raise ValueError('host is none')
        __tmp1._host = __tmp0
        __tmp1._port = port

        if kinds is None:
            raise ValueError('kinds is none')
        __tmp1._kinds = kinds

    @property
    def address(__tmp1) :
        return __tmp1._host + ":" + __typ1(__tmp1._port)

    @property
    def __tmp0(__tmp1) :
        return __tmp1._host

    @property
    def port(__tmp1) -> int:
        return __tmp1._port

    @property
    def kinds(__tmp1) :
        return __tmp1._kinds


class __typ5(__typ3):
    def __init__(__tmp1, __tmp0, port, kinds):
        super().__init__(__tmp0, port, kinds)


class __typ4(__typ3):
    def __init__(__tmp1, __tmp0, port, kinds):
        super().__init__(__tmp0, port, kinds)


class __typ2(__typ3):
    def __init__(__tmp1, __tmp0: __typ1, port: <FILL>, kinds: List[__typ1]):
        super().__init__(__tmp0, port, kinds)
