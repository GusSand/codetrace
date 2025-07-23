from graphx.configurations.app import settings
from graphx.core.rest.definitions import NodeConfigurator
from graphx.core.rest.resources import NodeCollection, EdgeCollection
from registry.services import BootableService, Container


class __typ0(BootableService):
    def boot(__tmp1, __tmp0: <FILL>):
        falcon = __tmp0.get(settings.Props.FALCON)

        provider = __tmp0.get(settings.Props.DI_PROVIDER)
        provider.add_configurator(NodeConfigurator)
        injector = provider.get_injector()

        falcon.add_route("/v1/nodes", injector.get(NodeCollection))
        falcon.add_route("/v1/edges", injector.get(EdgeCollection))
