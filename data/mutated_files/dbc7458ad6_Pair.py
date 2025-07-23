from parser.pair import Pair
from typing import Iterable

from calculator.distance_calculator import DistanceCalculator


def __tmp4(__tmp2: Iterable[Pair], __tmp1: int) :
    empty_embedding = [[0] * __tmp1]
    return (Pair(pair.image1 or empty_embedding,
                 pair.image2 or empty_embedding,
                 pair.is_match) for pair in __tmp2)


def __tmp5(__tmp2) :
    return (pair for pair in __tmp2 if pair.image1 and pair.image2)


def __tmp3(__tmp2,
                  __tmp6) :
    return (__tmp0(pair, __tmp6) for pair in __tmp2)


def __tmp0(pair: <FILL>, __tmp6) -> Pair:
    possible_pairs = [Pair(image1, image2, pair.is_match)
                      for image1 in pair.image1
                      for image2 in pair.image2]
    distance_calculator = DistanceCalculator(__tmp6)
    distances = distance_calculator.calculate(possible_pairs)
    distance_criteria = min if pair.is_match else max
    index, _ = distance_criteria(enumerate(distances), key=lambda x: x[1])
    return possible_pairs[index]
