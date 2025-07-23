from abc import ABCMeta
from typing import List

from protoactor.cluster.member_status import MemberStatus


class ClusterTopologyEvent():
    def __init__(__tmp2, __tmp3):
        if __tmp3 is None:
            raise ValueError('statuses is empty')
        __tmp2._statuses = __tmp3

    @property
    def __tmp3(__tmp2) -> List[MemberStatus]:
        return __tmp2._statuses


class AbstractMemberStatusEvent(metaclass=ABCMeta):
    def __init__(__tmp2, __tmp0: <FILL>, port, __tmp1):
        if __tmp0 is None:
            raise ValueError('host is none')
        __tmp2._host = __tmp0
        __tmp2._port = port

        if __tmp1 is None:
            raise ValueError('kinds is none')
        __tmp2._kinds = __tmp1

    @property
    def address(__tmp2) :
        return __tmp2._host + ":" + str(__tmp2._port)

    @property
    def __tmp0(__tmp2) :
        return __tmp2._host

    @property
    def port(__tmp2) :
        return __tmp2._port

    @property
    def __tmp1(__tmp2) :
        return __tmp2._kinds


class MemberJoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0, port, __tmp1):
        super().__init__(__tmp0, port, __tmp1)


class __typ0(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0: str, port, __tmp1):
        super().__init__(__tmp0, port, __tmp1)


class MemberLeftEvent(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0, port, __tmp1):
        super().__init__(__tmp0, port, __tmp1)
