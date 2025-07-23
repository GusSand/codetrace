from typing import TypeAlias
__typ0 : TypeAlias = "int"
from abc import ABCMeta
from typing import List

from protoactor.сluster.member_status import MemberStatus


class __typ1():
    def __init__(__tmp0, __tmp1):
        if __tmp1 is None:
            raise ValueError('statuses is empty')
        __tmp0._statuses = __tmp1

    @property
    def __tmp1(__tmp0) -> List[MemberStatus]:
        return __tmp0._statuses


class __typ3(metaclass=ABCMeta):
    def __init__(__tmp0, __tmp3: str, port: __typ0, __tmp2: List[str]):
        if __tmp3 is None:
            raise ValueError('host is none')
        __tmp0._host = __tmp3
        __tmp0._port = port

        if __tmp2 is None:
            raise ValueError('kinds is none')
        __tmp0._kinds = __tmp2

    @property
    def __tmp4(__tmp0) :
        return __tmp0._host + ":" + str(__tmp0._port)

    @property
    def __tmp3(__tmp0) :
        return __tmp0._host

    @property
    def port(__tmp0) -> __typ0:
        return __tmp0._port

    @property
    def __tmp2(__tmp0) -> List[str]:
        return __tmp0._kinds


class __typ5(__typ3):
    def __init__(__tmp0, __tmp3: str, port: __typ0, __tmp2):
        super().__init__(__tmp3, port, __tmp2)


class __typ4(__typ3):
    def __init__(__tmp0, __tmp3: <FILL>, port, __tmp2: List[str]):
        super().__init__(__tmp3, port, __tmp2)


class __typ2(__typ3):
    def __init__(__tmp0, __tmp3, port: __typ0, __tmp2):
        super().__init__(__tmp3, port, __tmp2)
