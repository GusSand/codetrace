from protoactor.actor import PID


class __typ1:
    def __tmp0(self, watcher: <FILL>, writer: PID):
        self.watcher = watcher
        self.writer = writer

class __typ3:
    def __tmp0(self, address):
        self.address = address


class EndpointTerminatedEvent:
    def __tmp0(self, address):
        self.address = address


class __typ5:
    def __tmp0(self, watcher: PID, watchee: PID):
        self.watcher = watcher
        self.watchee = watchee


class __typ0:
    def __tmp0(self, watcher, watchee: PID):
        self.watcher = watcher
        self.watchee = watchee


class __typ2:
    def __tmp0(self, watcher: PID, watchee: PID):
        self.watcher = watcher
        self.watchee = watchee


class __typ6:
    def __tmp0(self, header, message, target, sender, serializer_id):
        self.header = header
        self.message = message
        self.target = target
        self.sender = sender
        self.serializer_id = serializer_id


class __typ4:
    def __tmp0(self, type_name, json):
        if type_name is None:
            raise TypeError("type_name")
        if json is None:
            raise TypeError("json")

        self.type_name = type_name
        self.json = json
