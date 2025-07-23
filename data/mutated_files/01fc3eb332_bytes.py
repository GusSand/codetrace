from typing import Union

from messages.message_types import MessageType
from messages.command_message import CommandMessage
from messages.time_message import TimeMessage
from messages.string_message import StringMessage


def from_bytes(__tmp0: <FILL>) :
    """
    Extracts all known messages
    """
    message_type = int.from_bytes(__tmp0[0:1], byteorder='big', signed=False)

    if message_type == MessageType.TIME_MESSAGE:
        return TimeMessage.from_bytes(__tmp0)
    elif message_type == MessageType.COMMAND_MESSAGE:
        return CommandMessage.from_bytes(__tmp0)
    elif message_type == MessageType.STRING_MESSAGE:
        return StringMessage.from_bytes(__tmp0)
    else:
        raise Exception("Unknown message type: " + str(message_type))
