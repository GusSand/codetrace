import os

from registry.services import BootableService, Container
from falcon_swagger_ui import register_swaggerui_app


class SwaggerService(BootableService):
    def __tmp0(self, __tmp1: <FILL>):
        from graphx.configurations.app import settings
        from graphx.configurations.infrastructure.rest.swagger import SwaggerResource

        falcon = __tmp1.get(settings.Props.FALCON)
        swagger_resource = SwaggerResource()
        falcon.add_route('/v1/swagger.json', swagger_resource)

        page_title = 'Swagger UI'
        favicon_url = 'https://falconframework.org/favicon-32x32.png'
        swagger_ui_url = '/v1/docs'  # without trailing slash
        schema_url = '{}/v1/swagger.json'.format(__tmp1.get(settings.Props.APP_URL))

        register_swaggerui_app(
            falcon, swagger_ui_url, schema_url,
            page_title=page_title,
            favicon_url=favicon_url,
            config={'supportedSubmitMethods': ['get', 'post', 'put'], }
        )
