import abc
from meerkat.domain.post.entities.post import Post
from meerkat.domain.post.value_objects import Id


class __typ0(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __tmp0(__tmp2, post):
        """ Saves the post to the data-store
            Args:
                post (Post): The post entity

            Returns:
                None
        """
        pass

    @abc.abstractmethod
    def __tmp1(__tmp2, id: <FILL>) :
        """ Saves the post to the data-store
            Args:
                id (Id): post id

            Returns:
                None

            Raises:
                EntityNotFoundException: if the specified entity cannot be found
        """
        pass
