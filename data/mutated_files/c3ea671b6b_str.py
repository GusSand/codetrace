from typing import TypeAlias
__typ0 : TypeAlias = "Pair"
__typ1 : TypeAlias = "int"
from parser.pair import Pair
from typing import Iterable

from calculator.distance_calculator import DistanceCalculator


def __tmp2(__tmp1, embedding_size) :
    empty_embedding = [[0] * embedding_size]
    return (__typ0(pair.image1 or empty_embedding,
                 pair.image2 or empty_embedding,
                 pair.is_match) for pair in __tmp1)


def __tmp3(__tmp1) :
    return (pair for pair in __tmp1 if pair.image1 and pair.image2)


def filter_target(__tmp1,
                  __tmp4) :
    return (__tmp0(pair, __tmp4) for pair in __tmp1)


def __tmp0(pair, __tmp4: <FILL>) :
    possible_pairs = [__typ0(image1, image2, pair.is_match)
                      for image1 in pair.image1
                      for image2 in pair.image2]
    distance_calculator = DistanceCalculator(__tmp4)
    distances = distance_calculator.calculate(possible_pairs)
    distance_criteria = min if pair.is_match else max
    index, _ = distance_criteria(enumerate(distances), key=lambda x: x[1])
    return possible_pairs[index]
