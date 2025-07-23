from typing import TypeAlias
__typ1 : TypeAlias = "str"
from typing import List


class __typ3:
    def __tmp4(__tmp1, __tmp7: __typ1):
        __tmp1._name = __tmp7

    @property
    def __tmp7(__tmp1) :
        return __tmp1._name


class __typ4:
    def __tmp4(__tmp1, __tmp6: <FILL>, __tmp7: __typ1, __tmp2, __tmp5: __typ1):
        __tmp1._index = __tmp6
        __tmp1._name = __tmp7
        __tmp1._input_name = __tmp2
        __tmp1._output_name = __tmp5

    @property
    def __tmp6(__tmp1) -> int:
        return __tmp1._index

    @property
    def __tmp7(__tmp1) -> __typ1:
        return __tmp1._name

    @property
    def __tmp2(__tmp1) -> __typ1:
        return __tmp1._input_name

    @property
    def __tmp5(__tmp1) -> __typ1:
        return __tmp1._output_name


class __typ0:
    def __tmp4(__tmp1, __tmp7: __typ1, __tmp0: List[__typ1] = None):
        if __tmp0 is None:
            __tmp0 = []
        __tmp1._name = __tmp7
        __tmp1._methods = __tmp0

    @property
    def __tmp7(__tmp1) :
        return __tmp1._name

    @property
    def __tmp0(__tmp1) :
        return __tmp1._methods


class __typ2:
    def __tmp4(__tmp1, messages=None, __tmp3=None):
        if __tmp3 is None:
            __tmp3 = []
        if messages is None:
            messages = []
        __tmp1._messages = messages
        __tmp1._services = __tmp3

    @property
    def messages(__tmp1) -> List[__typ3]:
        return __tmp1._messages

    @property
    def __tmp3(__tmp1) -> List[__typ0]:
        return __tmp1._services
