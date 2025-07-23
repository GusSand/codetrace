from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "bytes"
__typ3 : TypeAlias = "bool"
from abc import abstractmethod, ABCMeta
from typing import List


class AbstractMemberStatusValue(metaclass=ABCMeta):
    @abstractmethod
    def is_same(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class AbstractMemberStatusValueSerializer(metaclass=ABCMeta):
    @abstractmethod
    def __tmp2(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def from_value_bytes(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class MemberStatus:
    def __init__(__tmp1, member_id, host, port: <FILL>, kinds, alive,
                 status_value):
        __tmp1._member_id = member_id
        if host is None:
            raise ValueError('host not set')
        __tmp1._host = host
        if kinds is None:
            raise ValueError('kinds not set')
        __tmp1._kinds = kinds
        __tmp1._port = port
        __tmp1._alive = alive
        __tmp1._status_value = status_value

    @property
    def address(__tmp1) :
        return __tmp1._host + ':' + __typ1(__tmp1._port)

    @property
    def member_id(__tmp1) :
        return __tmp1._member_id

    @property
    def host(__tmp1) :
        return __tmp1._host

    @property
    def port(__tmp1) :
        return __tmp1._port

    @property
    def kinds(__tmp1) :
        return __tmp1._kinds

    @property
    def alive(__tmp1) :
        return __tmp1._alive

    @property
    def status_value(__tmp1) :
        return __tmp1._status_value


class __typ0(AbstractMemberStatusValueSerializer):
    def __tmp2(__tmp1, __tmp0) :
        return None

    def from_value_bytes(__tmp1, __tmp0) :
        return None