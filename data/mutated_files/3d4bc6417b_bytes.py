from typing import TypeAlias
__typ0 : TypeAlias = "str"
from messages.message_types import MessageType


class __typ1:
    """
    Message which contains a string
    """

    def __tmp2(__tmp1, string):
        __tmp1.string = string

    def __tmp0(__tmp1):
        string_buf = __tmp1.string.encode('UTF-8')
        type_buf = MessageType.STRING_MESSAGE.to_bytes(
            1, byteorder='big', signed=False)

        return type_buf + string_buf

    @staticmethod
    def from_bytes(__tmp3: <FILL>) :
        msg_type = int.from_bytes(__tmp3[0:1], byteorder='big', signed=False)
        assert msg_type == MessageType.STRING_MESSAGE

        string = __tmp3[1:].decode('utf-8')

        return __typ1(string)
