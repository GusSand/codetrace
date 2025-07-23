from abc import ABC, abstractmethod

from enum import Enum


class __typ1(Enum):
    pass


class Container(object):
    def __tmp5(__tmp1):
        __tmp1.vars = {}

    def set(__tmp1, prop, __tmp4):
        __tmp1.vars[prop] = __tmp4

    def __tmp3(__tmp1, __tmp6):
        return __tmp1.vars[__tmp6]


class BootableService(ABC):

    @abstractmethod
    def boot(__tmp1, __tmp0: <FILL>):
        raise NotImplemented('Service not implemented')


class __typ0(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __tmp5(__tmp1):
        __tmp1.services: list = []

    def __tmp2(__tmp1, service):
        __tmp1.services.append(service)

    def boot(__tmp1, __tmp0):
        for service in __tmp1.services:
            service.boot(__tmp0)
