from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
__typ6 : TypeAlias = "bytes"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    def is_same(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    def to_value_bytes(__tmp1, __tmp0: __typ1) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def from_value_bytes(__tmp1, __tmp0) -> __typ1:
        raise NotImplementedError("Should Implement this method")


class __typ2:
    def __init__(__tmp1, __tmp3: <FILL>, __tmp2: str, port: __typ0, kinds, __tmp4: __typ4,
                 status_value: __typ1):
        __tmp1._member_id = __tmp3
        if __tmp2 is None:
            raise ValueError('host not set')
        __tmp1._host = __tmp2
        if kinds is None:
            raise ValueError('kinds not set')
        __tmp1._kinds = kinds
        __tmp1._port = port
        __tmp1._alive = __tmp4
        __tmp1._status_value = status_value

    @property
    def address(__tmp1) :
        return __tmp1._host + ':' + str(__tmp1._port)

    @property
    def __tmp3(__tmp1) -> str:
        return __tmp1._member_id

    @property
    def __tmp2(__tmp1) -> str:
        return __tmp1._host

    @property
    def port(__tmp1) -> __typ0:
        return __tmp1._port

    @property
    def kinds(__tmp1) -> List[str]:
        return __tmp1._kinds

    @property
    def __tmp4(__tmp1) -> __typ4:
        return __tmp1._alive

    @property
    def status_value(__tmp1) :
        return __tmp1._status_value


class __typ5(__typ3):
    def to_value_bytes(__tmp1, __tmp0) -> __typ6:
        return None

    def from_value_bytes(__tmp1, __tmp0: __typ6) -> __typ1:
        return None