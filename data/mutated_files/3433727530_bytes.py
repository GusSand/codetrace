from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    def __tmp6(__tmp1, __tmp0) -> __typ3:
        raise NotImplementedError("Should Implement this method")


class AbstractMemberStatusValueSerializer(metaclass=ABCMeta):
    @abstractmethod
    def __tmp5(__tmp1, __tmp0: __typ1) -> bytes:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def __tmp3(__tmp1, __tmp0: bytes) -> __typ1:
        raise NotImplementedError("Should Implement this method")


class MemberStatus:
    def __init__(__tmp1, member_id, __tmp2: __typ2, port: __typ0, kinds: List[__typ2], __tmp4,
                 __tmp7: __typ1):
        __tmp1._member_id = member_id
        if __tmp2 is None:
            raise ValueError('host not set')
        __tmp1._host = __tmp2
        if kinds is None:
            raise ValueError('kinds not set')
        __tmp1._kinds = kinds
        __tmp1._port = port
        __tmp1._alive = __tmp4
        __tmp1._status_value = __tmp7

    @property
    def address(__tmp1) -> __typ2:
        return __tmp1._host + ':' + __typ2(__tmp1._port)

    @property
    def member_id(__tmp1) -> __typ2:
        return __tmp1._member_id

    @property
    def __tmp2(__tmp1) -> __typ2:
        return __tmp1._host

    @property
    def port(__tmp1) -> __typ0:
        return __tmp1._port

    @property
    def kinds(__tmp1) :
        return __tmp1._kinds

    @property
    def __tmp4(__tmp1) -> __typ3:
        return __tmp1._alive

    @property
    def __tmp7(__tmp1) :
        return __tmp1._status_value


class __typ4(AbstractMemberStatusValueSerializer):
    def __tmp5(__tmp1, __tmp0: __typ1) -> bytes:
        return None

    def __tmp3(__tmp1, __tmp0: <FILL>) -> __typ1:
        return None