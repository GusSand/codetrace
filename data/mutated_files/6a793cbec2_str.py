from typing import TypeAlias
__typ1 : TypeAlias = "object"
__typ0 : TypeAlias = "bool"
"""add type check utils"""
from typing import Union, Optional


def type_check(__tmp2, __tmp1: <FILL>) :
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
    if hasattr(__tmp2, '__class__') and hasattr(__tmp2.__class__, '__name__'):
        return __tmp2.__class__.__name__ == __tmp1
    return False


def __tmp0(__tmp2) -> str:
    if __tmp2:
        return __tmp2
    return ''
