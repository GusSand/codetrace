from abc import ABCMeta
from typing import List

from protoactor.cluster.member_status import MemberStatus


class ClusterTopologyEvent():
    def __init__(__tmp0, __tmp1: List[MemberStatus]):
        if __tmp1 is None:
            raise ValueError('statuses is empty')
        __tmp0._statuses = __tmp1

    @property
    def __tmp1(__tmp0) :
        return __tmp0._statuses


class AbstractMemberStatusEvent(metaclass=ABCMeta):
    def __init__(__tmp0, __tmp3, port: <FILL>, __tmp2):
        if __tmp3 is None:
            raise ValueError('host is none')
        __tmp0._host = __tmp3
        __tmp0._port = port

        if __tmp2 is None:
            raise ValueError('kinds is none')
        __tmp0._kinds = __tmp2

    @property
    def __tmp4(__tmp0) -> str:
        return __tmp0._host + ":" + str(__tmp0._port)

    @property
    def __tmp3(__tmp0) -> str:
        return __tmp0._host

    @property
    def port(__tmp0) -> int:
        return __tmp0._port

    @property
    def __tmp2(__tmp0) :
        return __tmp0._kinds


class MemberJoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp0, __tmp3: str, port: int, __tmp2: List[str]):
        super().__init__(__tmp3, port, __tmp2)


class MemberRejoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp0, __tmp3: str, port: int, __tmp2: List[str]):
        super().__init__(__tmp3, port, __tmp2)


class __typ0(AbstractMemberStatusEvent):
    def __init__(__tmp0, __tmp3: str, port: int, __tmp2: List[str]):
        super().__init__(__tmp3, port, __tmp2)
