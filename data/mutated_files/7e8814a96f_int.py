from typing import TypeAlias
__typ1 : TypeAlias = "str"
from abc import ABCMeta
from typing import List

from protoactor.cluster.member_status import MemberStatus


class ClusterTopologyEvent():
    def __init__(__tmp2, statuses: List[MemberStatus]):
        if statuses is None:
            raise ValueError('statuses is empty')
        __tmp2._statuses = statuses

    @property
    def statuses(__tmp2) :
        return __tmp2._statuses


class AbstractMemberStatusEvent(metaclass=ABCMeta):
    def __init__(__tmp2, __tmp0: __typ1, port: int, __tmp1):
        if __tmp0 is None:
            raise ValueError('host is none')
        __tmp2._host = __tmp0
        __tmp2._port = port

        if __tmp1 is None:
            raise ValueError('kinds is none')
        __tmp2._kinds = __tmp1

    @property
    def __tmp3(__tmp2) -> __typ1:
        return __tmp2._host + ":" + __typ1(__tmp2._port)

    @property
    def __tmp0(__tmp2) :
        return __tmp2._host

    @property
    def port(__tmp2) :
        return __tmp2._port

    @property
    def __tmp1(__tmp2) :
        return __tmp2._kinds


class __typ0(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0: __typ1, port, __tmp1: List[__typ1]):
        super().__init__(__tmp0, port, __tmp1)


class __typ2(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0, port: <FILL>, __tmp1):
        super().__init__(__tmp0, port, __tmp1)


class __typ3(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0, port, __tmp1: List[__typ1]):
        super().__init__(__tmp0, port, __tmp1)
