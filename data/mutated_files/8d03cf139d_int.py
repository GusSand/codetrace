from typing import TypeAlias
__typ0 : TypeAlias = "float"
from enum import Enum
from enum import auto


class EvaluationMetric:
    def __tmp1(self,
                 __tmp2: __typ0,
                 recall: __typ0,
                 precision: __typ0) -> None:
        self._accuracy = __tmp2
        self._recall = recall
        self._precision = precision

    @property
    def __tmp2(self):
        return self._accuracy

    @property
    def recall(self):
        return self._recall

    @property
    def precision(self):
        return self._precision

    def __str__(self):
        return 'Evaluation Metrics - accuracy: {:.2f}, \
recall: {:.2f}, precision: {:.2f}'.format(self._accuracy,
                                          self._recall,
                                          self._precision)


class __typ1:
    def __tmp1(self,
                 __tmp0: int,
                 num_missing: <FILL>,
                 percentage_missing) -> None:
        self._num_expected = __tmp0
        self._num_missing = num_missing
        self._percentage_missing = percentage_missing

    @property
    def __tmp0(self):
        return self._num_expected

    @property
    def num_missing(self):
        return self._num_missing

    @property
    def percentage_missing(self):
        return self._percentage_missing

    def __str__(self):
        return 'Face Vector Metrics - num_expected: {}, \
num_missing: {}, percentage_missing: {:.2f}'.format(self._num_expected,
                                                    self.num_missing,
                                                    self.percentage_missing)


class DistanceMetric(Enum):
    ANGULAR_DISTANCE = auto()
    EUCLIDEAN_SQUARED = auto()


class ThresholdMetric(Enum):
    ACCURACY = auto()
    PRECISION = auto()
    RECALL = auto()
    F1 = auto()


class DistanceMetricException(Exception):
    pass


class ThresholdMetricException(Exception):
    pass
