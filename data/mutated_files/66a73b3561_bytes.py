from datetime import datetime as dt

from messages.message_types import MessageType


class __typ0:
    """
    Message which contains the current timestamp
    """

    def __init__(__tmp0):
        __tmp0.datetime: dt = dt.now()

    def __bytes__(__tmp0):
        type_buf = MessageType.TIME_MESSAGE.to_bytes(
            1, byteorder='big', signed=False)

        # POSIX timestamp as int
        ts = int(dt.now().timestamp()*1000)
        ts_buf = ts.to_bytes(8, byteorder='big', signed=False)
        return type_buf + ts_buf

    @staticmethod
    def from_bytes(bb: <FILL>):
        msg_type = int.from_bytes(bb[0:1], byteorder='big', signed=False)
        assert msg_type == MessageType.TIME_MESSAGE
        assert len(bb) == 9

        ts = int.from_bytes(bb[1:9], byteorder='big', signed=False)
        time = dt.fromtimestamp(ts/1000)

        tm = __typ0()
        tm.datetime = time
        return tm
