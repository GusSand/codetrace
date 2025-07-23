# Python imports
from abc import ABC
import logging
from typing import Iterable, Callable, List, Collection

# Data science imports
from pandas import DataFrame, Series

# Local imports
from data_processing.data_loader import DataLoader

LOGGER = logging.getLogger(__name__)


class Combiner(ABC):
    """
    A base class for any Combiners
    """

    def __init__(__tmp1, score_function: Callable[[DataFrame, DataFrame], float]):
        __tmp1.score_function = score_function

    def __tmp0(__tmp1, __tmp3: DataFrame, __tmp6: List[DataFrame]) :
        """
        Combines predictions to provide a better aggregate prediction.

        Arguments:
            * labels: The correct data
            * predictions: The list of predictions by the models

        Returns:
            * A list of float with the individual weights. Sum of the weights will be 1
        """
        return NotImplemented


class NaiveCombiner(Combiner):
    """
    This combines models in a dumb way to optimise multiple datasets.
    """

    def __init__(
        __tmp1,
        score_function: Callable[[DataFrame, DataFrame], float],
        number_of_steps: int = 10,
    ):
        """
        Initialises the Naive Combiner. 
        Arguments:
            * All arguments for the BaseCombiner
            * number_of_steps: The number of steps to use. Default 10.
        """
        assert number_of_steps >= 1, "Step size must be at least 1"
        super().__init__(score_function)

        __tmp1.number_of_steps = number_of_steps

    def __tmp0(__tmp1, __tmp4: <FILL>, __tmp6: List[DataFrame]) -> List[float]:
        """
        Combines a number of output predictions to provide a weighted output.
        This is a naivie combiner that assigns weights from 0 until and including step per prediction.

        Arguments:
            * labels: The correct data
            * predictions: The list of predictions by the models

        Returns:
            * A list of float with the individual weights. Sum of the weights will be 1
        """
        LOGGER.info("Starting to combine")

        __tmp2 = len(__tmp6)
        total_number_of_steps = (__tmp1.number_of_steps + 1) ** (__tmp2)
        indexes = __tmp6[0].index
        columns = __tmp6[0].columns

        best_score: float = -1
        best_weights: List[float] = []
        best_Y: Series = None

        for i in range(1, total_number_of_steps + 1):
            weights = __tmp1._convert_number_to_weights(
                i, __tmp1.number_of_steps, __tmp2
            )
            Y_attempt = DataFrame(0, index=indexes, columns=columns, dtype="float64")
            for j, test in enumerate(__tmp6):
                Y_attempt += test * weights[j]
            score = __tmp1.score_function(__tmp4, Y_attempt)
            if score > best_score:
                best_score = score
                best_weights = weights
                best_Y = Y_attempt
                LOGGER.info(
                    f"Got a new best score for a combination: {best_score} with weights {best_weights}"
                )

        LOGGER.info(
            f"Ended the combination job: score {best_score} with weights {best_weights}"
        )
        return best_weights

    def _convert_number_to_weights(
        __tmp1, index: int, __tmp5: int, __tmp2: int
    ):
        weights = []
        new_index = index
        for i in range(__tmp2):
            new_weight = (new_index % (__tmp5 + 1)) / (
                __tmp5 + 1
            )
            weights.append(new_weight)
            new_index = new_index // (__tmp5 + 1)
        total_weight = sum(weight for weight in weights)
        if total_weight != 0:
            weights = [weight / total_weight for weight in weights]
        return weights
