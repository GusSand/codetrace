from typing import List

from movies.models import Movie
from .interface import MLProxyInterface


class __typ0(MLProxyInterface):
    """
    Here we will be "mocking" the the ProductionMLProxy
    so we don't depend on the MLService in development
    """

    @staticmethod
    def get_challenge(n: int) :
        # return the n first movies
        return list(Movie.objects.all())[:n]

    @staticmethod
    def __tmp0(n: <FILL>) -> List[Movie]:
        # return the n last movies
        return list(Movie.objects.all())[-n:]
