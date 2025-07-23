import json

import falcon
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon import Request
from falcon.response import Response
from falcon_apispec import FalconPlugin

from meerkat.configurations.infrastructure.rest.health import HealthSchema, HealthCheck
from meerkat.entrypoints.rest.post.resources import PostCollection, Post
from meerkat.entrypoints.rest.post.schemas import PostSchema


class __typ0:
    def __tmp3(__tmp2):
        from meerkat.configurations.app.settings import Props
        from meerkat.configurations.app.main import app
        from meerkat.configurations.app.main import container
        # todo: should be moved to env vars
        __tmp2.spec = APISpec(title='meerkat',
                            version='1.0.0',
                            openapi_version='2.0',
                            plugins=[
                                FalconPlugin(app),
                                MarshmallowPlugin(),
                            ])
        injector = container.get(Props.DI_PROVIDER).get_injector()

        __tmp2.spec.components.schema('Health', schema=injector.get(HealthSchema))
        __tmp2.spec.path(resource=injector.get(HealthCheck))

        __tmp2.spec.components.schema('Post', schema=injector.get(PostSchema))

        __tmp2.spec.path(resource=injector.get(PostCollection))
        __tmp2.spec.path(resource=injector.get(Post))

    def __tmp0(__tmp2, __tmp1, resp: <FILL>):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(__tmp2.spec.to_dict(), ensure_ascii=False)
