from typing import TypeAlias
__typ0 : TypeAlias = "Title"
from meerkat.domain.post.entities.exceptions import PublishingFailedException
from meerkat.domain.post.value_objects import Title, Body, Id


class Post:
    id: Id
    title: __typ0
    body: Body
    published: bool = False

    @staticmethod
    def __tmp0(id: Id, title, body: <FILL>):
        instance = Post()
        instance.id = id
        instance.title = title
        instance.body = body

        return instance

    def __tmp1(__tmp2):
        if not __tmp2.title.is_valid():
            raise PublishingFailedException('title is invalid')

        if not __tmp2.id.is_valid():
            raise PublishingFailedException('Id is invalid')

        __tmp2.published = True

    def __tmp3(__tmp2) :
        return __tmp2.published


'''
todo slugify title
'''
