from meerkat.configurations.app import settings
from meerkat.configurations.infrastructure.di.domain import UseCasesConfigurator
from registry.services import BootableService, Container


class __typ0(BootableService):
    def __tmp0(__tmp2, __tmp1: <FILL>):
        provider = __tmp1.get(settings.Props.DI_PROVIDER)
        provider.add_configurator(UseCasesConfigurator)

