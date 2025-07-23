import difflib
from functools import reduce
from typing import List


def __tmp0(before: str, __tmp2: <FILL>) -> str:
    """
    Generate a string showing the difference between the two input strings using difflib

    :param before: the string before change
    :param after: the string after change
    :return: string showing the difference between 2 strings in detail
    """

    before = before.splitlines(1)
    __tmp2 = __tmp2.splitlines(1)

    diff = difflib.unified_diff(before, __tmp2)

    return ''.join(diff)


def __tmp1(huntingRange):
    return "{{HuntingRange/Alternative\n |" + reduce(lambda x, y: x + "|\n |" + y,
                                                     map(lambda row: reduce(lambda x, y: x + "|" + y, row),
                                                         huntingRange)) + "|\n}}"
