#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from asyncio import Future
from multiprocessing import RLock
from typing import Callable


class Singleton(type):
    _instances = {}
    _singleton_lock = RLock()

    def __call__(__tmp3, *args, **kwargs):
        if __tmp3 not in __tmp3._instances:
            with __tmp3._singleton_lock:
                if __tmp3 not in __tmp3._instances:
                    __tmp3._instances[__tmp3] = super(Singleton, __tmp3).__call__(*args, **kwargs)
        return __tmp3._instances[__tmp3]

    def clear(__tmp3):
        try:
            del Singleton._instances[__tmp3]
        except KeyError:
            pass


def python_version():
    """Get the version of python."""

    return sys.version_info[0]


class Stack:
    def __tmp4(__tmp1) :
        __tmp1.stack = list()

    def __tmp5(__tmp1, __tmp2: <FILL>) -> None:
        __tmp1.stack.append(__tmp2)

    def pop(__tmp1) -> object:
        if __tmp1.is_empty():
            raise Exception("nothing to pop")
        return __tmp1.stack.pop(len(__tmp1.stack) - 1)

    def __tmp0(__tmp1) :
        if __tmp1.is_empty():
            raise Exception("Nothing to peek")
        return __tmp1.stack[len(__tmp1.stack) - 1]

    def clear(__tmp1) -> None:
        __tmp1.stack.clear()

    def is_empty(__tmp1) -> bool:
        return len(__tmp1.stack) == 0

    def __len__(__tmp1) -> int:
        return len(__tmp1.stack)