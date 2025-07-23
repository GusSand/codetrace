from abc import ABC, abstractmethod

from enum import Enum


class __typ1(Enum):
    pass


class Container(object):
    def __tmp7(__tmp1):
        __tmp1.vars = {}

    def set(__tmp1, __tmp3, __tmp5):
        __tmp1.vars[__tmp3] = __tmp5

    def __tmp4(__tmp1, __tmp8: __typ1):
        return __tmp1.vars[__tmp8]


class BootableService(ABC):

    @abstractmethod
    def boot(__tmp1, __tmp0: <FILL>):
        raise NotImplemented('Service not implemented')

    def post_boot(__tmp1, __tmp0):
        pass


class __typ0(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __tmp7(__tmp1):
        __tmp1.services: list = []

    def __tmp2(__tmp1, __tmp6: BootableService):
        __tmp1.services.append(__tmp6)

    def boot(__tmp1, __tmp0):
        for __tmp6 in __tmp1.services:
            __tmp6.boot(__tmp0)

        for __tmp6 in __tmp1.services:
            __tmp6.post_boot(__tmp0)
