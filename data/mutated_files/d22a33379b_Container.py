from registry.services import BootableService, Container
from mongoengine import connect


class __typ0(BootableService):

    def boot(__tmp0, container: <FILL>):
        from meerkat.configurations.app.settings import Props

        host = container.get(Props.MONGO_HOST)
        port = int(container.get(Props.MONGO_PORT))
        db = container.get(Props.MONGO_DB)

        connect(db, host=host, port=port)

