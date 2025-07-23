from graphx.configurations.infrastructure.db.definitions import GraphConfigurator
from registry.services import BootableService, Container


class __typ0(BootableService):

    def __tmp0(__tmp2, __tmp1: <FILL>):
        from graphx.configurations.app.settings import Props

        url = __tmp1.get(Props.NEO_URL)
        username = __tmp1.get(Props.NEO_USERNAME)
        password = __tmp1.get(Props.NEO_PASSWORD)

        configurator = GraphConfigurator(url, username, password)

        provider = __tmp1.get(Props.DI_PROVIDER)
        provider.add_configurator(configurator)

