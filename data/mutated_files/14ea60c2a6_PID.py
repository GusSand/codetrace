from protoactor.actor import PID


class __typ1:
    def __tmp1(__tmp0, watcher, writer: PID):
        __tmp0.watcher = watcher
        __tmp0.writer = writer

class __typ4:
    def __tmp1(__tmp0, address):
        __tmp0.address = address


class __typ0:
    def __tmp1(__tmp0, address):
        __tmp0.address = address


class __typ5:
    def __tmp1(__tmp0, watcher: PID, watchee: PID):
        __tmp0.watcher = watcher
        __tmp0.watchee = watchee


class RemoteWatch:
    def __tmp1(__tmp0, watcher: PID, watchee: <FILL>):
        __tmp0.watcher = watcher
        __tmp0.watchee = watchee


class __typ2:
    def __tmp1(__tmp0, watcher, watchee: PID):
        __tmp0.watcher = watcher
        __tmp0.watchee = watchee


class __typ6:
    def __tmp1(__tmp0, header, message, target, sender, serializer_id):
        __tmp0.header = header
        __tmp0.message = message
        __tmp0.target = target
        __tmp0.sender = sender
        __tmp0.serializer_id = serializer_id


class __typ3:
    def __tmp1(__tmp0, type_name, json):
        if type_name is None:
            raise TypeError("type_name")
        if json is None:
            raise TypeError("json")

        __tmp0.type_name = type_name
        __tmp0.json = json
