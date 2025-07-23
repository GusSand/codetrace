from typing import TypeAlias
__typ1 : TypeAlias = "DataFrame"
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

    def __init__(self, score_function: Callable[[__typ1, __typ1], float]):
        self.score_function = score_function

    def combine(self, lables: __typ1, __tmp1) :
        """
        Combines predictions to provide a better aggregate prediction.

        Arguments:
            * labels: The correct data
            * predictions: The list of predictions by the models

        Returns:
            * A list of float with the individual weights. Sum of the weights will be 1
        """
        return NotImplemented


class __typ0(Combiner):
    """
    This combines models in a dumb way to optimise multiple datasets.
    """

    def __init__(
        self,
        score_function,
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

        self.number_of_steps = number_of_steps

    def combine(self, __tmp0: __typ1, __tmp1) :
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

        number_of_predictions = len(__tmp1)
        total_number_of_steps = (self.number_of_steps + 1) ** (number_of_predictions)
        indexes = __tmp1[0].index
        columns = __tmp1[0].columns

        best_score: float = -1
        best_weights: List[float] = []
        best_Y: Series = None

        for i in range(1, total_number_of_steps + 1):
            weights = self._convert_number_to_weights(
                i, self.number_of_steps, number_of_predictions
            )
            Y_attempt = __typ1(0, index=indexes, columns=columns, dtype="float64")
            for j, test in enumerate(__tmp1):
                Y_attempt += test * weights[j]
            score = self.score_function(__tmp0, Y_attempt)
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
        self, index, steps_per_prediction, number_of_predictions: <FILL>
    ):
        weights = []
        new_index = index
        for i in range(number_of_predictions):
            new_weight = (new_index % (steps_per_prediction + 1)) / (
                steps_per_prediction + 1
            )
            weights.append(new_weight)
            new_index = new_index // (steps_per_prediction + 1)
        total_weight = sum(weight for weight in weights)
        if total_weight != 0:
            weights = [weight / total_weight for weight in weights]
        return weights
