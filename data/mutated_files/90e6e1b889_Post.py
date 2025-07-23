from typing import TypeAlias
__typ1 : TypeAlias = "PostDocument"
from meerkat.data_providers.database.mongo.documents import PostDocument
from meerkat.domain.post.entities import Post
from meerkat.domain.post.value_objects import Id, Title, Body


class __typ0:
    def __tmp1(__tmp2, post: <FILL>) :
        return __typ1(id=post.id.value, title=post.title.value, body=post.body.value,
                            published=post.is_published())

    def __tmp0(__tmp2, __tmp3) :
        post = Post.create(Id(__tmp3.id), Title(__tmp3.title), Body(__tmp3.body))
        post.published = __tmp3.published
        return post
