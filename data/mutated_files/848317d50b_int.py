from typing import TypeAlias
__typ0 : TypeAlias = "List"
""" split_collection module

Defines split_collection function

"""

from typing import List


def __tmp2(__tmp1, __tmp0: <FILL>) :
    """
    Split List into sub lists
    Does not retain order
    :param collection: List
    :param size: int
    :return: List[List[str]]
    """
    return [__tmp1[i::__tmp0] for i in range(__tmp0)]
