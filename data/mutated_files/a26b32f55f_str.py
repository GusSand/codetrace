from messages.message_types import MessageType


class __typ0:
    """
    Message which contains a string
    """

    def __init__(__tmp0, string: <FILL>):
        __tmp0.string = string

    def __tmp1(__tmp0):
        string_buf = __tmp0.string.encode('UTF-8')
        type_buf = MessageType.STRING_MESSAGE.to_bytes(
            1, byteorder='big', signed=False)

        return type_buf + string_buf

    @staticmethod
    def from_bytes(bb: bytes) :
        msg_type = int.from_bytes(bb[0:1], byteorder='big', signed=False)
        assert msg_type == MessageType.STRING_MESSAGE

        string = bb[1:].decode('utf-8')

        return __typ0(string)
