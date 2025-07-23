from typing import Any

from protoactor.actor.message_header import MessageHeader

is_import = False
if is_import:
    from protoactor.actor import PID


class MessageEnvelope:
    def __tmp6(__tmp0, message: object, sender: 'PID' = None, header: MessageHeader = None) :
        __tmp0._message = message
        __tmp0._sender = sender
        __tmp0._header = header

    @property
    def message(__tmp0) -> object:
        return __tmp0._message

    @property
    def sender(__tmp0) :
        return __tmp0._sender

    @property
    def header(__tmp0) :
        return __tmp0._header

    @staticmethod
    def __tmp1(message):
        if isinstance(message, MessageEnvelope):
            return message
        return MessageEnvelope(message)

    def __tmp3(__tmp0, sender: 'PID'):
        return MessageEnvelope(__tmp0.message, sender, __tmp0.header)

    def __tmp4(__tmp0, message):
        return MessageEnvelope(message, __tmp0.sender, __tmp0.header)

    def __tmp8(__tmp0, header: MessageHeader = None, key: str = None, value: str = None):
        if header is not None and key is None and value is None:
            return MessageEnvelope(__tmp0.message, __tmp0.sender, header)
        elif header is None and key is not None and value is not None:
            message_header = __tmp0.header
            if message_header is None:
                message_header = MessageHeader()
            header = message_header.extend(key=key, value=value)
            return MessageEnvelope(__tmp0.message, __tmp0.sender, header)
        else:
            raise ValueError('Incorrect input value')

    def __tmp7(__tmp0, items=None):
        message_header = __tmp0.header
        if message_header is None:
            message_header = MessageHeader()
        header = message_header.extend(items=items)
        return MessageEnvelope(__tmp0.message, __tmp0.sender, header)

    @staticmethod
    def __tmp5(message: Any) -> Any:
        if isinstance(message, MessageEnvelope):
            return message.message, message.sender, message.header
        return message, None, None

    @staticmethod
    def unwrap_header(message) :
        if isinstance(message, MessageEnvelope) and message.header is not None:
            return message.header
        return MessageHeader.empty()

    @staticmethod
    def unwrap_message(message: Any) :
        if isinstance(message, MessageEnvelope):
            return message.message
        else:
            return message

    @staticmethod
    def __tmp2(message: <FILL>) -> 'PID':
        if isinstance(message, MessageEnvelope):
            return message.sender
        else:
            return None
