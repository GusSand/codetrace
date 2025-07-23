from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
from abc import abstractmethod, ABCMeta
from typing import List


class __typ2(metaclass=ABCMeta):
    @abstractmethod
    def __tmp10(__tmp1, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class AbstractMemberStatusValueSerializer(metaclass=ABCMeta):
    @abstractmethod
    def __tmp7(__tmp1, __tmp0: __typ2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    def __tmp6(__tmp1, __tmp0) -> __typ2:
        raise NotImplementedError("Should Implement this method")


class __typ3:
    def __tmp8(__tmp1, __tmp4, __tmp3: <FILL>, port, __tmp2: List[str], __tmp5,
                 __tmp11):
        __tmp1._member_id = __tmp4
        if __tmp3 is None:
            raise ValueError('host not set')
        __tmp1._host = __tmp3
        if __tmp2 is None:
            raise ValueError('kinds not set')
        __tmp1._kinds = __tmp2
        __tmp1._port = port
        __tmp1._alive = __tmp5
        __tmp1._status_value = __tmp11

    @property
    def __tmp9(__tmp1) -> str:
        return __tmp1._host + ':' + str(__tmp1._port)

    @property
    def __tmp4(__tmp1) :
        return __tmp1._member_id

    @property
    def __tmp3(__tmp1) :
        return __tmp1._host

    @property
    def port(__tmp1) :
        return __tmp1._port

    @property
    def __tmp2(__tmp1) :
        return __tmp1._kinds

    @property
    def __tmp5(__tmp1) :
        return __tmp1._alive

    @property
    def __tmp11(__tmp1) :
        return __tmp1._status_value


class __typ0(AbstractMemberStatusValueSerializer):
    def __tmp7(__tmp1, __tmp0) :
        return None

    def __tmp6(__tmp1, __tmp0) :
        return None