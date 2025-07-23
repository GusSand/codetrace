""" split_collection module

Defines split_collection function

"""

from typing import List


def split_collection(__tmp0: <FILL>, size) :
    """
    Split List into sub lists
    Does not retain order
    :param collection: List
    :param size: int
    :return: List[List[str]]
    """
    return [__tmp0[i::size] for i in range(size)]
