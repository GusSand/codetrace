import os

from registry.services import BootableService, Container


class __typ0(BootableService):

    def __tmp0(__tmp2, __tmp1: <FILL>):
        from meerkat.configurations.app.settings import Props

        __tmp1.set(Props.APP_URL, os.environ.get(Props.APP_URL.value))

        __tmp1.set(Props.MONGO_HOST, os.environ.get(Props.MONGO_HOST.value))
        __tmp1.set(Props.MONGO_PORT, os.environ.get(Props.MONGO_PORT.value))
        __tmp1.set(Props.MONGO_DB, os.environ.get(Props.MONGO_DB.value))
