from typing import TypeAlias
__typ1 : TypeAlias = "Post"
__typ0 : TypeAlias = "PublishPostUseCase"
import json
import logging
import uuid

import falcon

from meerkat.configurations.app.middlewares import HTTPValidationError
from meerkat.domain.post.use_cases import AddNewPostUseCase, PublishPostUseCase
from meerkat.domain.post.use_cases.add_new_post import AddNewPostCommand
from meerkat.domain.post.use_cases.publish_post import PublishPostCommand
from meerkat.domain.post.value_objects import Id
from meerkat.entrypoints.rest.post.schemas import PostSchema, AddNewPostSchema


class PostCollection:
    schema = PostSchema()
    post_schema = AddNewPostSchema()

    def __tmp1(__tmp2, add_new_post):
        __tmp2.add_new_post = add_new_post

    def on_post(__tmp2, __tmp0, __tmp3):
        """Add new a post
                ---
                    tags:
                        - Posts
                    summary: Add new post
                    consumes:
                        - application/json
                    produces:
                        - application/json
                    parameters:
                        - in: body
                          schema: AddNewPostSchema
                    responses:
                        201:
                            description: post added
                            schema: PostSchema
                        415:
                            description: Unsupported Media Type

        """
        # PostCollection.schema = AddNewPostSchema
        try:
            request_json = __tmp0.context['json']
        except KeyError:
            raise HTTPValidationError(status=falcon.status_codes.HTTP_400, errors=["Empty request body"])

        command = AddNewPostCommand(**request_json)

        post = __tmp2.add_new_post.exec(command)

        __tmp3.status = falcon.HTTP_201
        __tmp3.body = json.dumps(PostSchema.from_domain_object(post))


class __typ1:
    schema = PostSchema()

    def __tmp1(__tmp2, publish_post):
        __tmp2.publish_post_usecase = publish_post

    def on_put(__tmp2, __tmp0: falcon.Request, __tmp3, id: <FILL>) -> None:
        """
               ---
               summary: Publish post
               tags:
                   - Posts
               parameters:
                   - in: path
                     name: id
               produces:
                   - application/json
               responses:
                   204:
                       description: post published
        """

        command = PublishPostCommand(Id(uuid.UUID(id)))

        __tmp2.publish_post_usecase.exec(command)

        __tmp3.status = falcon.HTTP_204
