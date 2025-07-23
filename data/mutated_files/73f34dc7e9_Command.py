from messages.message_types import Command, MessageType


class __typ0:
    """
    Message which contains a single command

    Commands are used to signal/trigger certain events, they do not
    contain data apart from their type
    """

    def __init__(__tmp0, command: <FILL>):
        __tmp0.command = command

    def __tmp1(__tmp0):
        type_buf = MessageType.COMMAND_MESSAGE.to_bytes(
            1, byteorder='big', signed=False)
        command_buf = __tmp0.command.to_bytes(1, byteorder='big', signed=False)
        return type_buf + command_buf

    @staticmethod
    def from_bytes(__tmp2):
        msg_type = int.from_bytes(__tmp2[0:1], byteorder='big', signed=False)
        assert msg_type == MessageType.COMMAND_MESSAGE
        assert len(__tmp2) == 2

        command = Command(int.from_bytes(
            __tmp2[1:2], byteorder='big', signed=False))
        return __typ0(command)
