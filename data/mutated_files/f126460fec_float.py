from parser.pair import Pair
from typing import Callable
from typing import Iterable
from typing import Union
from typing import cast

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from calculator.calculator import Calculator
from calculator.distance_calculator import DistanceCalculator
from metrics.metrics import DistanceMetric
from metrics.metrics import ThresholdMetric
from metrics.metrics import ThresholdMetricException


# pylint: disable=too-few-public-methods
class ThresholdCalculator(Calculator):

    # pylint: disable=too-many-arguments
    def __tmp4(__tmp0,
                 __tmp6,
                 __tmp2: Union[str, ThresholdMetric],
                 __tmp3: <FILL>,
                 __tmp5,
                 __tmp1) -> None:
        if isinstance(__tmp2, str):
            __tmp0._threshold_metric = getattr(ThresholdMetric,
                                             cast(str, __tmp2))
        else:
            __tmp0._threshold_metric = __tmp2
        __tmp0._distance_metric = __tmp6
        __tmp0._threshold_start = __tmp3
        __tmp0._threshold_end = __tmp5
        __tmp0._threshold_step = __tmp1

    def calculate(__tmp0, pairs) -> float:
        threshold_scorer = __tmp0._get_threshold_scorer()
        dist = DistanceCalculator(__tmp0._distance_metric).calculate(pairs)
        labels = [pair.is_match for pair in pairs]
        best_score = float('-inf')
        best_threshold_index = 0
        thresholds = np.arange(__tmp0._threshold_start,
                               __tmp0._threshold_end,
                               __tmp0._threshold_step)
        for i, threshold in enumerate(thresholds):
            predictions = np.less(dist, threshold)
            score = threshold_scorer(labels, predictions)
            if score > best_score:
                best_score = score
                best_threshold_index = i
        return thresholds[best_threshold_index]

    def _get_threshold_scorer(
            __tmp0) -> Callable[[np.ndarray, np.ndarray], float]:
        if __tmp0._threshold_metric == ThresholdMetric.ACCURACY:
            return accuracy_score
        if __tmp0._threshold_metric == ThresholdMetric.PRECISION:
            return precision_score
        if __tmp0._threshold_metric == ThresholdMetric.RECALL:
            return recall_score
        if __tmp0._threshold_metric == ThresholdMetric.F1:
            return f1_score
        metrics = [str(metric) for metric in ThresholdMetric]
        err = f"Undefined {ThresholdMetric.__qualname__}. \
Choose from {metrics}"
        raise ThresholdMetricException(err)
