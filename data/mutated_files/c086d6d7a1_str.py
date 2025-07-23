from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import List


class __typ3:
    def __tmp1(__tmp0, __tmp2):
        __tmp0._name = __tmp2

    @property
    def __tmp2(__tmp0) :
        return __tmp0._name


class __typ4:
    def __tmp1(__tmp0, index, __tmp2, input_name, output_name):
        __tmp0._index = index
        __tmp0._name = __tmp2
        __tmp0._input_name = input_name
        __tmp0._output_name = output_name

    @property
    def index(__tmp0) :
        return __tmp0._index

    @property
    def __tmp2(__tmp0) :
        return __tmp0._name

    @property
    def input_name(__tmp0) -> str:
        return __tmp0._input_name

    @property
    def output_name(__tmp0) :
        return __tmp0._output_name


class __typ1:
    def __tmp1(__tmp0, __tmp2: <FILL>, methods: List[str] = None):
        if methods is None:
            methods = []
        __tmp0._name = __tmp2
        __tmp0._methods = methods

    @property
    def __tmp2(__tmp0) -> str:
        return __tmp0._name

    @property
    def methods(__tmp0) -> List[__typ4]:
        return __tmp0._methods


class __typ2:
    def __tmp1(__tmp0, messages=None, services=None):
        if services is None:
            services = []
        if messages is None:
            messages = []
        __tmp0._messages = messages
        __tmp0._services = services

    @property
    def messages(__tmp0) :
        return __tmp0._messages

    @property
    def services(__tmp0) :
        return __tmp0._services
