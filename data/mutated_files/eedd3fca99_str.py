from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import List


class ProtoMessage:
    def __tmp4(__tmp0, __tmp7):
        __tmp0._name = __tmp7

    @property
    def __tmp7(__tmp0) :
        return __tmp0._name


class ProtoMethod:
    def __tmp4(__tmp0, __tmp6, __tmp7, __tmp1, __tmp5: <FILL>):
        __tmp0._index = __tmp6
        __tmp0._name = __tmp7
        __tmp0._input_name = __tmp1
        __tmp0._output_name = __tmp5

    @property
    def __tmp6(__tmp0) -> __typ0:
        return __tmp0._index

    @property
    def __tmp7(__tmp0) :
        return __tmp0._name

    @property
    def __tmp1(__tmp0) :
        return __tmp0._input_name

    @property
    def __tmp5(__tmp0) :
        return __tmp0._output_name


class ProtoService:
    def __tmp4(__tmp0, __tmp7, methods: List[str] = None):
        if methods is None:
            methods = []
        __tmp0._name = __tmp7
        __tmp0._methods = methods

    @property
    def __tmp7(__tmp0) :
        return __tmp0._name

    @property
    def methods(__tmp0) :
        return __tmp0._methods


class ProtoFile:
    def __tmp4(__tmp0, __tmp3=None, __tmp2=None):
        if __tmp2 is None:
            __tmp2 = []
        if __tmp3 is None:
            __tmp3 = []
        __tmp0._messages = __tmp3
        __tmp0._services = __tmp2

    @property
    def __tmp3(__tmp0) -> List[ProtoMessage]:
        return __tmp0._messages

    @property
    def __tmp2(__tmp0) :
        return __tmp0._services
