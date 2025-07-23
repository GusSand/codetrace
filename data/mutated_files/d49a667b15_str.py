from typing import List


class ProtoMessage:
    def __tmp5(__tmp1, __tmp8: str):
        __tmp1._name = __tmp8

    @property
    def __tmp8(__tmp1) -> str:
        return __tmp1._name


class ProtoMethod:
    def __tmp5(__tmp1, __tmp7: int, __tmp8: <FILL>, __tmp2, __tmp6: str):
        __tmp1._index = __tmp7
        __tmp1._name = __tmp8
        __tmp1._input_name = __tmp2
        __tmp1._output_name = __tmp6

    @property
    def __tmp7(__tmp1) -> int:
        return __tmp1._index

    @property
    def __tmp8(__tmp1) -> str:
        return __tmp1._name

    @property
    def __tmp2(__tmp1) -> str:
        return __tmp1._input_name

    @property
    def __tmp6(__tmp1) -> str:
        return __tmp1._output_name


class ProtoService:
    def __tmp5(__tmp1, __tmp8: str, __tmp0: List[str] = None):
        if __tmp0 is None:
            __tmp0 = []
        __tmp1._name = __tmp8
        __tmp1._methods = __tmp0

    @property
    def __tmp8(__tmp1) :
        return __tmp1._name

    @property
    def __tmp0(__tmp1) -> List[ProtoMethod]:
        return __tmp1._methods


class __typ0:
    def __tmp5(__tmp1, __tmp4=None, __tmp3=None):
        if __tmp3 is None:
            __tmp3 = []
        if __tmp4 is None:
            __tmp4 = []
        __tmp1._messages = __tmp4
        __tmp1._services = __tmp3

    @property
    def __tmp4(__tmp1) -> List[ProtoMessage]:
        return __tmp1._messages

    @property
    def __tmp3(__tmp1) -> List[ProtoService]:
        return __tmp1._services
