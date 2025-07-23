from parser.pair import Pair
from typing import Iterable

from calculator.distance_calculator import DistanceCalculator


def __tmp4(__tmp2: Iterable[Pair], __tmp1) :
    empty_embedding = [[0] * __tmp1]
    return (Pair(pair.image1 or empty_embedding,
                 pair.image2 or empty_embedding,
                 pair.is_match) for pair in __tmp2)


def remove_empty(__tmp2) :
    return (pair for pair in __tmp2 if pair.image1 and pair.image2)


def __tmp3(__tmp2,
                  __tmp5: <FILL>) :
    return (__tmp0(pair, __tmp5) for pair in __tmp2)


def __tmp0(pair, __tmp5) :
    possible_pairs = [Pair(image1, image2, pair.is_match)
                      for image1 in pair.image1
                      for image2 in pair.image2]
    distance_calculator = DistanceCalculator(__tmp5)
    distances = distance_calculator.calculate(possible_pairs)
    distance_criteria = min if pair.is_match else max
    index, _ = distance_criteria(enumerate(distances), key=lambda x: x[1])
    return possible_pairs[index]
