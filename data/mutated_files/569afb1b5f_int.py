from typing import TypeAlias
__typ5 : TypeAlias = "bytes"
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ0(metaclass=ABCMeta):
    @abstractmethod
    def is_same(__tmp0, val) -> __typ4:
        raise NotImplementedError("Should Implement this method")


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    def to_value_bytes(__tmp0, val: __typ0) -> __typ5:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def __tmp1(__tmp0, val: __typ5) -> __typ0:
        raise NotImplementedError("Should Implement this method")


class __typ2:
    def __init__(__tmp0, member_id: __typ1, host: __typ1, port: <FILL>, kinds: List[__typ1], alive: __typ4,
                 status_value: __typ0):
        __tmp0._member_id = member_id
        if host is None:
            raise ValueError('host not set')
        __tmp0._host = host
        if kinds is None:
            raise ValueError('kinds not set')
        __tmp0._kinds = kinds
        __tmp0._port = port
        __tmp0._alive = alive
        __tmp0._status_value = status_value

    @property
    def address(__tmp0) :
        return __tmp0._host + ':' + __typ1(__tmp0._port)

    @property
    def member_id(__tmp0) -> __typ1:
        return __tmp0._member_id

    @property
    def host(__tmp0) -> __typ1:
        return __tmp0._host

    @property
    def port(__tmp0) -> int:
        return __tmp0._port

    @property
    def kinds(__tmp0) -> List[__typ1]:
        return __tmp0._kinds

    @property
    def alive(__tmp0) -> __typ4:
        return __tmp0._alive

    @property
    def status_value(__tmp0) -> __typ0:
        return __tmp0._status_value


class NullMemberStatusValueSerializer(__typ3):
    def to_value_bytes(__tmp0, val: __typ0) -> __typ5:
        return None

    def __tmp1(__tmp0, val) -> __typ0:
        return None