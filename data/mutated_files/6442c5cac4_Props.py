from typing import TypeAlias
__typ2 : TypeAlias = "Container"
from abc import ABC, abstractmethod

from enum import Enum


class Props(Enum):
    pass


class __typ2(object):
    def __init__(self):
        self.vars = {}

    def set(self, prop: <FILL>, __tmp0):
        self.vars[prop] = __tmp0

    def get(self, key: Props):
        return self.vars[key]


class __typ1(ABC):

    @abstractmethod
    def boot(self, container: __typ2):
        raise NotImplemented('Service not implemented')


class __typ0(object):
    """ Service registry is where to register bootable services to be booted
    """

    def __init__(self):
        self.services: list = []

    def __tmp1(self, service):
        self.services.append(service)

    def boot(self, container):
        for service in self.services:
            service.boot(container)
