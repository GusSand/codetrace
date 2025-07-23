from typing import TypeAlias
__typ1 : TypeAlias = "Id"
from injector import inject

from meerkat.domain.post.data_providers import PostDataProvider
from meerkat.domain.post.entities import Post
from meerkat.domain.post.value_objects import Id
from meerkat.domain.post.data_providers.exceptions import EntityNotFoundException
from meerkat.data_providers.database.mongo.transformers import PostDocumentTransformer
from meerkat.data_providers.database.mongo.documents import PostDocument


class __typ0(PostDataProvider):
    @inject
    def __tmp1(__tmp0, transformer):
        __tmp0.transformer = transformer

    def save(__tmp0, post: <FILL>):
        post_document = __tmp0.transformer.transform_to_document(post)
        post_document.save()

    def get(__tmp0, id: __typ1) -> Post:
        posts = PostDocument.objects(id=id.value)
        if posts.count() < 1:
            raise EntityNotFoundException('Cannot find document with id #{}'.format(str(id)))

        return __tmp0.transformer.transform_to_domain_object(next(posts))
