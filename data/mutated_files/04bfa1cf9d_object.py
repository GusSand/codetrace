"""add type check utils"""
from typing import Union, Optional


def __tmp1(__tmp3: <FILL>, __tmp2: str) :
    """
    circulation dependency problems can be resolved by TYPE_CHECKING,
    but this can not resolve NO type linting problems. eg:
        if isinstance(msg, Contact):
            pass
    in this problem, program don't import Contact at running time. So, it will
        throw a Exception, which will not be threw
    :param obj:
    :param type_name:
    :return:
    """
    if hasattr(__tmp3, '__class__') and hasattr(__tmp3.__class__, '__name__'):
        return __tmp3.__class__.__name__ == __tmp2
    return False


def __tmp0(__tmp3) :
    if __tmp3:
        return __tmp3
    return ''
