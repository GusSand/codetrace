from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "bytes"
__typ1 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    def is_same(__tmp1, __tmp0) -> __typ2:
        raise NotImplementedError("Should Implement this method")


class AbstractMemberStatusValueSerializer(metaclass=ABCMeta):
    @abstractmethod
    def __tmp4(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def __tmp3(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class MemberStatus:
    def __init__(__tmp1, member_id, host: <FILL>, port, __tmp2: List[str], alive,
                 status_value):
        __tmp1._member_id = member_id
        if host is None:
            raise ValueError('host not set')
        __tmp1._host = host
        if __tmp2 is None:
            raise ValueError('kinds not set')
        __tmp1._kinds = __tmp2
        __tmp1._port = port
        __tmp1._alive = alive
        __tmp1._status_value = status_value

    @property
    def address(__tmp1) :
        return __tmp1._host + ':' + str(__tmp1._port)

    @property
    def member_id(__tmp1) :
        return __tmp1._member_id

    @property
    def host(__tmp1) :
        return __tmp1._host

    @property
    def port(__tmp1) -> __typ1:
        return __tmp1._port

    @property
    def __tmp2(__tmp1) -> List[str]:
        return __tmp1._kinds

    @property
    def alive(__tmp1) :
        return __tmp1._alive

    @property
    def status_value(__tmp1) :
        return __tmp1._status_value


class NullMemberStatusValueSerializer(AbstractMemberStatusValueSerializer):
    def __tmp4(__tmp1, __tmp0) -> __typ0:
        return None

    def __tmp3(__tmp1, __tmp0) :
        return None