from typing import List

from movies.models import Movie
from .interface import MLProxyInterface


class DevMLProxy(MLProxyInterface):
    """
    Here we will be "mocking" the the ProductionMLProxy
    so we don't depend on the MLService in development
    """

    @staticmethod
    def get_challenge(n: <FILL>) :
        # return the n first movies
        return list(Movie.objects.all())[:n]

    @staticmethod
    def __tmp0(n) -> List[Movie]:
        # return the n last movies
        return list(Movie.objects.all())[-n:]
