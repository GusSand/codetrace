from typing import TypeAlias
__typ2 : TypeAlias = "int"
from typing import List


class ProtoMessage:
    def __tmp3(__tmp0, __tmp6: <FILL>):
        __tmp0._name = __tmp6

    @property
    def __tmp6(__tmp0) :
        return __tmp0._name


class __typ1:
    def __tmp3(__tmp0, __tmp5, __tmp6, __tmp1, __tmp4):
        __tmp0._index = __tmp5
        __tmp0._name = __tmp6
        __tmp0._input_name = __tmp1
        __tmp0._output_name = __tmp4

    @property
    def __tmp5(__tmp0) :
        return __tmp0._index

    @property
    def __tmp6(__tmp0) :
        return __tmp0._name

    @property
    def __tmp1(__tmp0) :
        return __tmp0._input_name

    @property
    def __tmp4(__tmp0) :
        return __tmp0._output_name


class __typ0:
    def __tmp3(__tmp0, __tmp6, methods: List[str] = None):
        if methods is None:
            methods = []
        __tmp0._name = __tmp6
        __tmp0._methods = methods

    @property
    def __tmp6(__tmp0) :
        return __tmp0._name

    @property
    def methods(__tmp0) :
        return __tmp0._methods


class ProtoFile:
    def __tmp3(__tmp0, __tmp2=None, services=None):
        if services is None:
            services = []
        if __tmp2 is None:
            __tmp2 = []
        __tmp0._messages = __tmp2
        __tmp0._services = services

    @property
    def __tmp2(__tmp0) :
        return __tmp0._messages

    @property
    def services(__tmp0) :
        return __tmp0._services
