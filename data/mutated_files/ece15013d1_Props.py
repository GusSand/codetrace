from typing import TypeAlias
__typ0 : TypeAlias = "Container"
from abc import ABC, abstractmethod

from enum import Enum


class Props(Enum):
    pass


class __typ0(object):
    def __tmp4(__tmp1):
        __tmp1.vars = {}

    def set(__tmp1, prop: Props, value):
        __tmp1.vars[prop] = value

    def __tmp0(__tmp1, __tmp5: <FILL>):
        return __tmp1.vars[__tmp5]


class BootableService(ABC):

    @abstractmethod
    def boot(__tmp1, container):
        raise NotImplemented('Service not implemented')


class Registry(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __tmp4(__tmp1):
        __tmp1.services: list = []

    def __tmp2(__tmp1, __tmp3):
        __tmp1.services.append(__tmp3)

    def boot(__tmp1, container):
        for __tmp3 in __tmp1.services:
            __tmp3.boot(container)
