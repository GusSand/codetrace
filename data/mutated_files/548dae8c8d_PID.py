from protoactor.actor import PID


class __typ2:
    def __init__(self, watcher, writer: PID):
        self.watcher = watcher
        self.writer = writer

class EndpointConnectedEvent:
    def __init__(self, address):
        self.address = address


class __typ0:
    def __init__(self, address):
        self.address = address


class RemoteTerminate:
    def __init__(self, watcher: <FILL>, watchee: PID):
        self.watcher = watcher
        self.watchee = watchee


class RemoteWatch:
    def __init__(self, watcher, watchee):
        self.watcher = watcher
        self.watchee = watchee


class RemoteUnwatch:
    def __init__(self, watcher, watchee: PID):
        self.watcher = watcher
        self.watchee = watchee


class RemoteDeliver:
    def __init__(self, header, message, target, sender, serializer_id):
        self.header = header
        self.message = message
        self.target = target
        self.sender = sender
        self.serializer_id = serializer_id


class __typ1:
    def __init__(self, type_name, json):
        if type_name is None:
            raise TypeError("type_name")
        if json is None:
            raise TypeError("json")

        self.type_name = type_name
        self.json = json
