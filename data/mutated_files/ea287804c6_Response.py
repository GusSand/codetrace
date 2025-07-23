from typing import TypeAlias
__typ0 : TypeAlias = "Request"
import json

import falcon
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon import Request
from falcon.response import Response
from falcon_apispec import FalconPlugin


from graphx.core.rest.resources import NodeCollection, EdgeCollection
from graphx.core.rest.schemas import Node, Edge


class __typ1:
    def __init__(self):
        from graphx.configurations.app.settings import Props
        from graphx.configurations.app.main import app
        from graphx.configurations.app.main import container
        # todo: should be moved to env vars
        self.spec = APISpec(title='graphx',
                            version='1.0.0',
                            openapi_version='2.0',
                            plugins=[
                                FalconPlugin(app),
                                MarshmallowPlugin(),
                            ])
        injector = container.get(Props.DI_PROVIDER).get_injector()

        self.spec.components.schema('Node', schema=injector.get(Node))
        self.spec.path(resource=injector.get(NodeCollection))

        self.spec.components.schema('Edge', schema=injector.get(Edge))
        self.spec.path(resource=injector.get(EdgeCollection))

    def __tmp0(self, req, resp: <FILL>):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(self.spec.to_dict(), ensure_ascii=False)
