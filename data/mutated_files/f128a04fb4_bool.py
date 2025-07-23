from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ4 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    def is_same(__tmp0, val: 'AbstractMemberStatusValue') -> bool:
        raise NotImplementedError("Should Implement this method")


class AbstractMemberStatusValueSerializer(metaclass=ABCMeta):
    @abstractmethod
    def to_value_bytes(__tmp0, val) -> __typ4:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def __tmp3(__tmp0, val) :
        raise NotImplementedError("Should Implement this method")


class __typ3:
    def __tmp4(__tmp0, __tmp2: __typ2, host, port, __tmp1, alive: <FILL>,
                 __tmp6):
        __tmp0._member_id = __tmp2
        if host is None:
            raise ValueError('host not set')
        __tmp0._host = host
        if __tmp1 is None:
            raise ValueError('kinds not set')
        __tmp0._kinds = __tmp1
        __tmp0._port = port
        __tmp0._alive = alive
        __tmp0._status_value = __tmp6

    @property
    def __tmp5(__tmp0) -> __typ2:
        return __tmp0._host + ':' + __typ2(__tmp0._port)

    @property
    def __tmp2(__tmp0) :
        return __tmp0._member_id

    @property
    def host(__tmp0) :
        return __tmp0._host

    @property
    def port(__tmp0) -> __typ0:
        return __tmp0._port

    @property
    def __tmp1(__tmp0) -> List[__typ2]:
        return __tmp0._kinds

    @property
    def alive(__tmp0) :
        return __tmp0._alive

    @property
    def __tmp6(__tmp0) :
        return __tmp0._status_value


class NullMemberStatusValueSerializer(AbstractMemberStatusValueSerializer):
    def to_value_bytes(__tmp0, val) :
        return None

    def __tmp3(__tmp0, val) :
        return None