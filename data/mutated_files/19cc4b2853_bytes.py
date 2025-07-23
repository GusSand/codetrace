import select
import socket

from messages import serialization
from mtexceptions.network_exceptions import ConnectionLost

# The number of bytes in which the length of a message is encoded.
# This value limits the size of supported messages. It is not exposed
# to the configuration file as it always needs to be the same for all
# PIs.
LENGTH = 2


class SocketWrapper:
    """
    Wraps a socket and makes sending and receiving messages easier

    Before sending a message, the socket adds the length of the message
    at the front, so that a message can be received completely. This
    length field is stripped before further processing.

    Effective message layout (with length in bytes)

    [Length : LENGTH][Message : N]
    """
    sock: socket.socket
    do_compress: bool
    select_timeout: float

    def __tmp4(__tmp1, __tmp0: socket.socket):
        __tmp1.sock = __tmp0

    def _send(__tmp1, __tmp5: <FILL>) :
        totalsent = 0
        while totalsent < len(__tmp5):
            # noinspection PyTypeChecker
            sent = __tmp1.sock.send(__tmp5[totalsent:])
            if sent == 0:
                __tmp1.sock.close()
                raise ConnectionLost("Connection was lost")
            totalsent = totalsent + sent
        return totalsent

    def _receive(__tmp1, __tmp3: int) -> bytes:
        chunks = []
        bytes_recd = 0
        while bytes_recd < __tmp3:
            chunk = __tmp1.sock.recv(__tmp3 - bytes_recd)
            if chunk == b'':
                __tmp1.sock.close()
                raise ConnectionLost("Connection was lost")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        # noinspection PyTypeChecker
        return b''.join(chunks)

    def __tmp6(__tmp1, __tmp7: bytes):
        # prepend the length of the message
        length: int = len(__tmp7)
        len_buf = length.to_bytes(LENGTH, byteorder='big', signed=False)
        __tmp1._send(len_buf + __tmp7)

    def __tmp2(__tmp1):
        # fetch length header first
        __tmp7 = __tmp1._receive(LENGTH)
        length = int.from_bytes(__tmp7, byteorder='big', signed=False)

        # get payload
        __tmp7 = __tmp1._receive(length)
        return serialization.from_bytes(__tmp7)

