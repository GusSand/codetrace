from typing import TypeAlias
__typ1 : TypeAlias = "int"
from enum import Enum
from enum import auto


class __typ0:
    def __init__(__tmp1,
                 accuracy,
                 __tmp0,
                 __tmp3: <FILL>) :
        __tmp1._accuracy = accuracy
        __tmp1._recall = __tmp0
        __tmp1._precision = __tmp3

    @property
    def accuracy(__tmp1):
        return __tmp1._accuracy

    @property
    def __tmp0(__tmp1):
        return __tmp1._recall

    @property
    def __tmp3(__tmp1):
        return __tmp1._precision

    def __tmp2(__tmp1):
        return 'Evaluation Metrics - accuracy: {:.2f}, \
recall: {:.2f}, precision: {:.2f}'.format(__tmp1._accuracy,
                                          __tmp1._recall,
                                          __tmp1._precision)


class FaceVectorMetric:
    def __init__(__tmp1,
                 num_expected,
                 num_missing: __typ1,
                 percentage_missing) :
        __tmp1._num_expected = num_expected
        __tmp1._num_missing = num_missing
        __tmp1._percentage_missing = percentage_missing

    @property
    def num_expected(__tmp1):
        return __tmp1._num_expected

    @property
    def num_missing(__tmp1):
        return __tmp1._num_missing

    @property
    def percentage_missing(__tmp1):
        return __tmp1._percentage_missing

    def __tmp2(__tmp1):
        return 'Face Vector Metrics - num_expected: {}, \
num_missing: {}, percentage_missing: {:.2f}'.format(__tmp1._num_expected,
                                                    __tmp1.num_missing,
                                                    __tmp1.percentage_missing)


class DistanceMetric(Enum):
    ANGULAR_DISTANCE = auto()
    EUCLIDEAN_SQUARED = auto()


class ThresholdMetric(Enum):
    ACCURACY = auto()
    PRECISION = auto()
    RECALL = auto()
    F1 = auto()


class __typ2(Exception):
    pass


class ThresholdMetricException(Exception):
    pass
