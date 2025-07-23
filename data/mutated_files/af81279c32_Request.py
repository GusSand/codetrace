from typing import TypeAlias
__typ1 : TypeAlias = "Response"
import json

import falcon
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon import Request
from falcon.response import Response
from falcon_apispec import FalconPlugin


from graphx.core.rest.resources import NodeCollection, EdgeCollection
from graphx.core.rest.schemas import Node, Edge


class __typ0:
    def __tmp3(__tmp2):
        from graphx.configurations.app.settings import Props
        from graphx.configurations.app.main import app
        from graphx.configurations.app.main import container
        # todo: should be moved to env vars
        __tmp2.spec = APISpec(title='graphx',
                            version='1.0.0',
                            openapi_version='2.0',
                            plugins=[
                                FalconPlugin(app),
                                MarshmallowPlugin(),
                            ])
        injector = container.get(Props.DI_PROVIDER).get_injector()

        __tmp2.spec.components.schema('Node', schema=injector.get(Node))
        __tmp2.spec.path(resource=injector.get(NodeCollection))

        __tmp2.spec.components.schema('Edge', schema=injector.get(Edge))
        __tmp2.spec.path(resource=injector.get(EdgeCollection))

    def __tmp0(__tmp2, __tmp1: <FILL>, resp: __typ1):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(__tmp2.spec.to_dict(), ensure_ascii=False)
