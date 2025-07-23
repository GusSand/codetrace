from abc import ABC, abstractmethod

from enum import Enum


class __typ1(Enum):
    pass


class Container(object):
    def __tmp3(__tmp2):
        __tmp2.vars = {}

    def set(__tmp2, prop: __typ1, value):
        __tmp2.vars[prop] = value

    def get(__tmp2, __tmp0):
        return __tmp2.vars[__tmp0]


class __typ2(ABC):

    @abstractmethod
    def boot(__tmp2, __tmp1: Container):
        raise NotImplemented('Service not implemented')


class __typ0(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __tmp3(__tmp2):
        __tmp2.services: list = []

    def register(__tmp2, service):
        __tmp2.services.append(service)

    def boot(__tmp2, __tmp1: <FILL>):
        for service in __tmp2.services:
            service.boot(__tmp1)
