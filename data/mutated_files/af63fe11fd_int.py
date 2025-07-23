from parser.pair import Pair
from typing import Iterable

from calculator.distance_calculator import DistanceCalculator


def fill_empty(__tmp1, embedding_size: <FILL>) :
    empty_embedding = [[0] * embedding_size]
    return (Pair(pair.image1 or empty_embedding,
                 pair.image2 or empty_embedding,
                 pair.is_match) for pair in __tmp1)


def remove_empty(__tmp1: Iterable[Pair]) :
    return (pair for pair in __tmp1 if pair.image1 and pair.image2)


def filter_target(__tmp1,
                  __tmp0) :
    return (_compute_target(pair, __tmp0) for pair in __tmp1)


def _compute_target(pair, __tmp0) -> Pair:
    possible_pairs = [Pair(image1, image2, pair.is_match)
                      for image1 in pair.image1
                      for image2 in pair.image2]
    distance_calculator = DistanceCalculator(__tmp0)
    distances = distance_calculator.calculate(possible_pairs)
    distance_criteria = min if pair.is_match else max
    index, _ = distance_criteria(enumerate(distances), key=lambda x: x[1])
    return possible_pairs[index]
