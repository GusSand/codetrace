from typing import TypeAlias
__typ1 : TypeAlias = "int"
from enum import Enum
from enum import auto


class __typ0:
    def __init__(__tmp1,
                 accuracy,
                 recall: <FILL>,
                 precision: float) :
        __tmp1._accuracy = accuracy
        __tmp1._recall = recall
        __tmp1._precision = precision

    @property
    def accuracy(__tmp1):
        return __tmp1._accuracy

    @property
    def recall(__tmp1):
        return __tmp1._recall

    @property
    def precision(__tmp1):
        return __tmp1._precision

    def __tmp2(__tmp1):
        return 'Evaluation Metrics - accuracy: {:.2f}, \
recall: {:.2f}, precision: {:.2f}'.format(__tmp1._accuracy,
                                          __tmp1._recall,
                                          __tmp1._precision)


class __typ6:
    def __init__(__tmp1,
                 __tmp0: __typ1,
                 num_missing,
                 percentage_missing) -> None:
        __tmp1._num_expected = __tmp0
        __tmp1._num_missing = num_missing
        __tmp1._percentage_missing = percentage_missing

    @property
    def __tmp0(__tmp1):
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


class __typ2(Enum):
    ANGULAR_DISTANCE = auto()
    EUCLIDEAN_SQUARED = auto()


class __typ4(Enum):
    ACCURACY = auto()
    PRECISION = auto()
    RECALL = auto()
    F1 = auto()


class __typ3(Exception):
    pass


class __typ5(Exception):
    pass
