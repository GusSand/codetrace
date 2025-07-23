from typing import TypeAlias
__typ0 : TypeAlias = "bool"
from meerkat.domain.post.entities.exceptions import PublishingFailedException
from meerkat.domain.post.value_objects import Title, Body, Id


class __typ1:
    id: Id
    title: Title
    body: Body
    published: __typ0 = False

    @staticmethod
    def create(id: <FILL>, title, body):
        instance = __typ1()
        instance.id = id
        instance.title = title
        instance.body = body

        return instance

    def publish(__tmp0):
        if not __tmp0.title.is_valid():
            raise PublishingFailedException('title is invalid')

        if not __tmp0.id.is_valid():
            raise PublishingFailedException('Id is invalid')

        __tmp0.published = True

    def __tmp1(__tmp0) -> __typ0:
        return __tmp0.published


'''
todo slugify title
'''
