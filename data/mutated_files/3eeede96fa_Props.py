from typing import TypeAlias
__typ2 : TypeAlias = "Container"
from abc import ABC, abstractmethod

from enum import Enum


class Props(Enum):
    pass


class __typ2(object):
    def __tmp6(__tmp1):
        __tmp1.vars = {}

    def set(__tmp1, __tmp3: <FILL>, __tmp5):
        __tmp1.vars[__tmp3] = __tmp5

    def __tmp2(__tmp1, __tmp7):
        return __tmp1.vars[__tmp7]


class __typ1(ABC):

    @abstractmethod
    def boot(__tmp1, __tmp0):
        raise NotImplemented('Service not implemented')

    def post_boot(__tmp1, __tmp0):
        pass


class __typ0(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __tmp6(__tmp1):
        __tmp1.services: list = []

    def __tmp4(__tmp1, service):
        __tmp1.services.append(service)

    def boot(__tmp1, __tmp0: __typ2):
        for service in __tmp1.services:
            service.boot(__tmp0)

        for service in __tmp1.services:
            service.post_boot(__tmp0)
