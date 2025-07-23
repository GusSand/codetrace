from abc import ABC, abstractmethod

from enum import Enum


class __typ0(Enum):
    pass


class Container(object):
    def __tmp6(__tmp1):
        __tmp1.vars = {}

    def set(__tmp1, __tmp3, __tmp4):
        __tmp1.vars[__tmp3] = __tmp4

    def get(__tmp1, __tmp7):
        return __tmp1.vars[__tmp7]


class __typ1(ABC):

    @abstractmethod
    def boot(__tmp1, __tmp0):
        raise NotImplemented('Service not implemented')

    def post_boot(__tmp1, __tmp0):
        pass


class Registry(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __tmp6(__tmp1):
        __tmp1.services: list = []

    def __tmp2(__tmp1, __tmp5):
        __tmp1.services.append(__tmp5)

    def boot(__tmp1, __tmp0: <FILL>):
        for __tmp5 in __tmp1.services:
            __tmp5.boot(__tmp0)

        for __tmp5 in __tmp1.services:
            __tmp5.post_boot(__tmp0)
