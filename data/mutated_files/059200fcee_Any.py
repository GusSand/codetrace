from typing import TypeAlias
__typ2 : TypeAlias = "object"
__typ1 : TypeAlias = "MessageHeader"
from typing import Any

from protoactor.actor.message_header import MessageHeader

is_import = False
if is_import:
    from protoactor.actor import PID


class __typ0:
    def __tmp3(__tmp2, message: __typ2, sender: 'PID' = None, header: __typ1 = None) :
        __tmp2._message = message
        __tmp2._sender = sender
        __tmp2._header = header

    @property
    def message(__tmp2) :
        return __tmp2._message

    @property
    def sender(__tmp2) -> 'PID':
        return __tmp2._sender

    @property
    def header(__tmp2) -> __typ1:
        return __tmp2._header

    @staticmethod
    def wrap(message):
        if isinstance(message, __typ0):
            return message
        return __typ0(message)

    def with_sender(__tmp2, sender: 'PID'):
        return __typ0(__tmp2.message, sender, __tmp2.header)

    def __tmp1(__tmp2, message: <FILL>):
        return __typ0(message, __tmp2.sender, __tmp2.header)

    def with_header(__tmp2, header: __typ1 = None, key: str = None, value: str = None):
        if header is not None and key is None and value is None:
            return __typ0(__tmp2.message, __tmp2.sender, header)
        elif header is None and key is not None and value is not None:
            message_header = __tmp2.header
            if message_header is None:
                message_header = __typ1()
            header = message_header.extend(key=key, value=value)
            return __typ0(__tmp2.message, __tmp2.sender, header)
        else:
            raise ValueError('Incorrect input value')

    def with_headers(__tmp2, items=None):
        message_header = __tmp2.header
        if message_header is None:
            message_header = __typ1()
        header = message_header.extend(items=items)
        return __typ0(__tmp2.message, __tmp2.sender, header)

    @staticmethod
    def unwrap(message) -> Any:
        if isinstance(message, __typ0):
            return message.message, message.sender, message.header
        return message, None, None

    @staticmethod
    def unwrap_header(message) :
        if isinstance(message, __typ0) and message.header is not None:
            return message.header
        return __typ1.empty()

    @staticmethod
    def __tmp0(message) :
        if isinstance(message, __typ0):
            return message.message
        else:
            return message

    @staticmethod
    def unwrap_sender(message: Any) -> 'PID':
        if isinstance(message, __typ0):
            return message.sender
        else:
            return None
