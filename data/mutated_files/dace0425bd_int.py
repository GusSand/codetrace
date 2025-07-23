from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
import select
import socket

from messages import serialization
from mtexceptions.network_exceptions import ConnectionLost

# The number of bytes in which the length of a message is encoded.
# This value limits the size of supported messages. It is not exposed
# to the configuration file as it always needs to be the same for all
# PIs.
LENGTH = 2


class __typ0:
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

    def __tmp1(__tmp0, _socket):
        __tmp0.sock = _socket

    def _send(__tmp0, msg) -> int:
        totalsent = 0
        while totalsent < len(msg):
            # noinspection PyTypeChecker
            sent = __tmp0.sock.send(msg[totalsent:])
            if sent == 0:
                __tmp0.sock.close()
                raise ConnectionLost("Connection was lost")
            totalsent = totalsent + sent
        return totalsent

    def _receive(__tmp0, nr_bytes: <FILL>) -> __typ1:
        chunks = []
        bytes_recd = 0
        while bytes_recd < nr_bytes:
            chunk = __tmp0.sock.recv(nr_bytes - bytes_recd)
            if chunk == b'':
                __tmp0.sock.close()
                raise ConnectionLost("Connection was lost")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        # noinspection PyTypeChecker
        return b''.join(chunks)

    def __tmp2(__tmp0, buf: __typ1):
        # prepend the length of the message
        length: int = len(buf)
        len_buf = length.to_bytes(LENGTH, byteorder='big', signed=False)
        __tmp0._send(len_buf + buf)

    def receive_message(__tmp0):
        # fetch length header first
        buf = __tmp0._receive(LENGTH)
        length = int.from_bytes(buf, byteorder='big', signed=False)

        # get payload
        buf = __tmp0._receive(length)
        return serialization.from_bytes(buf)

