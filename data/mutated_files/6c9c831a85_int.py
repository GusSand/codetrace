from typing import List
from abc import ABC, abstractmethod

from movies.models import Movie


class MLProxyInterface(ABC):
    @staticmethod
    @abstractmethod
    def __tmp0(n: <FILL>) -> List[Movie]:
        pass  # pragma: no cover

    @staticmethod
    @abstractmethod
    def get_recommendation(n) :
        pass  # pragma: no cover
