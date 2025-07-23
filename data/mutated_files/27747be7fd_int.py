from typing import TypeAlias
__typ0 : TypeAlias = "str"
from abc import ABCMeta
from typing import List

from protoactor.cluster.member_status import MemberStatus


class ClusterTopologyEvent():
    def __init__(__tmp1, statuses):
        if statuses is None:
            raise ValueError('statuses is empty')
        __tmp1._statuses = statuses

    @property
    def statuses(__tmp1) :
        return __tmp1._statuses


class AbstractMemberStatusEvent(metaclass=ABCMeta):
    def __init__(__tmp1, host: __typ0, port, __tmp0):
        if host is None:
            raise ValueError('host is none')
        __tmp1._host = host
        __tmp1._port = port

        if __tmp0 is None:
            raise ValueError('kinds is none')
        __tmp1._kinds = __tmp0

    @property
    def __tmp2(__tmp1) :
        return __tmp1._host + ":" + __typ0(__tmp1._port)

    @property
    def host(__tmp1) :
        return __tmp1._host

    @property
    def port(__tmp1) :
        return __tmp1._port

    @property
    def __tmp0(__tmp1) :
        return __tmp1._kinds


class MemberJoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp1, host, port, __tmp0):
        super().__init__(host, port, __tmp0)


class MemberRejoinedEvent(AbstractMemberStatusEvent):
    def __init__(__tmp1, host, port, __tmp0):
        super().__init__(host, port, __tmp0)


class MemberLeftEvent(AbstractMemberStatusEvent):
    def __init__(__tmp1, host, port: <FILL>, __tmp0):
        super().__init__(host, port, __tmp0)
