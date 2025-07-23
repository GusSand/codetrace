from typing import TypeAlias
__typ0 : TypeAlias = "int"
from enum import Enum
from enum import auto


class EvaluationMetric:
    def __tmp4(__tmp2,
                 __tmp0: <FILL>,
                 __tmp1,
                 __tmp5) :
        __tmp2._accuracy = __tmp0
        __tmp2._recall = __tmp1
        __tmp2._precision = __tmp5

    @property
    def __tmp0(__tmp2):
        return __tmp2._accuracy

    @property
    def __tmp1(__tmp2):
        return __tmp2._recall

    @property
    def __tmp5(__tmp2):
        return __tmp2._precision

    def __tmp6(__tmp2):
        return 'Evaluation Metrics - accuracy: {:.2f}, \
recall: {:.2f}, precision: {:.2f}'.format(__tmp2._accuracy,
                                          __tmp2._recall,
                                          __tmp2._precision)


class FaceVectorMetric:
    def __tmp4(__tmp2,
                 __tmp3,
                 num_missing,
                 percentage_missing) :
        __tmp2._num_expected = __tmp3
        __tmp2._num_missing = num_missing
        __tmp2._percentage_missing = percentage_missing

    @property
    def __tmp3(__tmp2):
        return __tmp2._num_expected

    @property
    def num_missing(__tmp2):
        return __tmp2._num_missing

    @property
    def percentage_missing(__tmp2):
        return __tmp2._percentage_missing

    def __tmp6(__tmp2):
        return 'Face Vector Metrics - num_expected: {}, \
num_missing: {}, percentage_missing: {:.2f}'.format(__tmp2._num_expected,
                                                    __tmp2.num_missing,
                                                    __tmp2.percentage_missing)


class __typ2(Enum):
    ANGULAR_DISTANCE = auto()
    EUCLIDEAN_SQUARED = auto()


class __typ1(Enum):
    ACCURACY = auto()
    PRECISION = auto()
    RECALL = auto()
    F1 = auto()


class DistanceMetricException(Exception):
    pass


class __typ3(Exception):
    pass
