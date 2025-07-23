from typing import TypeAlias
__typ0 : TypeAlias = "float"
from enum import Enum
from enum import auto


class EvaluationMetric:
    def __tmp3(__tmp0,
                 accuracy,
                 __tmp1: __typ0,
                 __tmp4) :
        __tmp0._accuracy = accuracy
        __tmp0._recall = __tmp1
        __tmp0._precision = __tmp4

    @property
    def accuracy(__tmp0):
        return __tmp0._accuracy

    @property
    def __tmp1(__tmp0):
        return __tmp0._recall

    @property
    def __tmp4(__tmp0):
        return __tmp0._precision

    def __tmp5(__tmp0):
        return 'Evaluation Metrics - accuracy: {:.2f}, \
recall: {:.2f}, precision: {:.2f}'.format(__tmp0._accuracy,
                                          __tmp0._recall,
                                          __tmp0._precision)


class FaceVectorMetric:
    def __tmp3(__tmp0,
                 __tmp2: <FILL>,
                 num_missing,
                 percentage_missing) :
        __tmp0._num_expected = __tmp2
        __tmp0._num_missing = num_missing
        __tmp0._percentage_missing = percentage_missing

    @property
    def __tmp2(__tmp0):
        return __tmp0._num_expected

    @property
    def num_missing(__tmp0):
        return __tmp0._num_missing

    @property
    def percentage_missing(__tmp0):
        return __tmp0._percentage_missing

    def __tmp5(__tmp0):
        return 'Face Vector Metrics - num_expected: {}, \
num_missing: {}, percentage_missing: {:.2f}'.format(__tmp0._num_expected,
                                                    __tmp0.num_missing,
                                                    __tmp0.percentage_missing)


class __typ1(Enum):
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
