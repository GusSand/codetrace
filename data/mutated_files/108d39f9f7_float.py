from typing import TypeAlias
__typ1 : TypeAlias = "int"
from enum import Enum
from enum import auto


class __typ0:
    def __init__(self,
                 accuracy,
                 recall,
                 __tmp0: float) :
        self._accuracy = accuracy
        self._recall = recall
        self._precision = __tmp0

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def recall(self):
        return self._recall

    @property
    def __tmp0(self):
        return self._precision

    def __str__(self):
        return 'Evaluation Metrics - accuracy: {:.2f}, \
recall: {:.2f}, precision: {:.2f}'.format(self._accuracy,
                                          self._recall,
                                          self._precision)


class __typ6:
    def __init__(self,
                 num_expected: __typ1,
                 num_missing,
                 percentage_missing: <FILL>) :
        self._num_expected = num_expected
        self._num_missing = num_missing
        self._percentage_missing = percentage_missing

    @property
    def num_expected(self):
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
