from typing import TypeAlias
__typ0 : TypeAlias = "str"
from abc import ABCMeta
from typing import List

from protoactor.сluster.member_status import MemberStatus


class ClusterTopologyEvent():
    def __init__(__tmp2, statuses: List[MemberStatus]):
        if statuses is None:
            raise ValueError('statuses is empty')
        __tmp2._statuses = statuses

    @property
    def statuses(__tmp2) -> List[MemberStatus]:
        return __tmp2._statuses


class AbstractMemberStatusEvent(metaclass=ABCMeta):
    def __init__(__tmp2, __tmp0: __typ0, port: int, __tmp1: List[__typ0]):
        if __tmp0 is None:
            raise ValueError('host is none')
        __tmp2._host = __tmp0
        __tmp2._port = port

        if __tmp1 is None:
            raise ValueError('kinds is none')
        __tmp2._kinds = __tmp1

    @property
    def address(__tmp2) -> __typ0:
        return __tmp2._host + ":" + __typ0(__tmp2._port)

    @property
    def __tmp0(__tmp2) -> __typ0:
        return __tmp2._host

    @property
    def port(__tmp2) -> int:
        return __tmp2._port

    @property
    def __tmp1(__tmp2) -> List[__typ0]:
        return __tmp2._kinds


class MemberJoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0, port: int, __tmp1: List[__typ0]):
        super().__init__(__tmp0, port, __tmp1)


class MemberRejoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0: __typ0, port: <FILL>, __tmp1: List[__typ0]):
        super().__init__(__tmp0, port, __tmp1)


class MemberLeftEvent(AbstractMemberStatusEvent):
    def __init__(__tmp2, __tmp0: __typ0, port: int, __tmp1):
        super().__init__(__tmp0, port, __tmp1)
