from typing import TypeAlias
__typ0 : TypeAlias = "bool"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    def is_same(__tmp1, __tmp0: 'AbstractMemberStatusValue') -> __typ0:
        raise NotImplementedError("Should Implement this method")


class AbstractMemberStatusValueSerializer(metaclass=ABCMeta):
    @abstractmethod
    def __tmp4(__tmp1, __tmp0: __typ1) -> bytes:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def from_value_bytes(__tmp1, __tmp0: <FILL>) -> __typ1:
        raise NotImplementedError("Should Implement this method")


class MemberStatus:
    def __tmp5(__tmp1, __tmp3, __tmp2: str, port: int, kinds: List[str], alive: __typ0,
                 __tmp7):
        __tmp1._member_id = __tmp3
        if __tmp2 is None:
            raise ValueError('host not set')
        __tmp1._host = __tmp2
        if kinds is None:
            raise ValueError('kinds not set')
        __tmp1._kinds = kinds
        __tmp1._port = port
        __tmp1._alive = alive
        __tmp1._status_value = __tmp7

    @property
    def __tmp6(__tmp1) -> str:
        return __tmp1._host + ':' + str(__tmp1._port)

    @property
    def __tmp3(__tmp1) -> str:
        return __tmp1._member_id

    @property
    def __tmp2(__tmp1) -> str:
        return __tmp1._host

    @property
    def port(__tmp1) -> int:
        return __tmp1._port

    @property
    def kinds(__tmp1) -> List[str]:
        return __tmp1._kinds

    @property
    def alive(__tmp1) -> __typ0:
        return __tmp1._alive

    @property
    def __tmp7(__tmp1) :
        return __tmp1._status_value


class NullMemberStatusValueSerializer(AbstractMemberStatusValueSerializer):
    def __tmp4(__tmp1, __tmp0) :
        return None

    def from_value_bytes(__tmp1, __tmp0: bytes) :
        return None