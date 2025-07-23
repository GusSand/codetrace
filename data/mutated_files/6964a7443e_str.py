from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""Helper functions for communicating with other peers"""
import asyncio
import socket
from socket import SHUT_WR
from typing import Any
from typing import Dict

import bencode  # type: ignore

from syncr_backend.constants import ERR_EXCEPTION
from syncr_backend.constants import ERR_INCOMPAT
from syncr_backend.constants import ERR_NEXIST
from syncr_backend.util.log_util import get_logger


logger = get_logger(__name__)


async def send_response(
    writer, __tmp1: Dict[Any, Any],
) :
    """
    Sends a response to a connection and then closes writing to that connection

    :param writer: StreamWriter to write to
    :param response: Dict[Any, Any] response
    :return: None
    """
    writer.write(bencode.encode(__tmp1))
    writer.write_eof()
    await writer.drain()


def __tmp0(conn: socket.socket, __tmp1) :
    """
    Syncronous version of send_response, using old style sockets

    :param conn: socket.accept() connection
    :param reponse: Dict[Any, Any] response
    :return: None
    """
    conn.send(bencode.encode(__tmp1))
    conn.shutdown(SHUT_WR)


class SyncrNetworkException(Exception):
    """Base exception for network errors"""
    pass


class NotExistException(SyncrNetworkException):
    """Requested object does not exist"""
    pass


class IncompatibleProtocolVersionException(SyncrNetworkException):
    """Version number of the protocol not compatible with request"""
    pass


class __typ1(SyncrNetworkException):
    """Other end experienced an unhandled exception"""
    pass


class NoPeersException(SyncrNetworkException):
    """No peers found or provided to a request function"""
    pass


def __tmp2(
    errno,
) -> None:
    """Raises an error based on the errno"""
    logger.debug("Raising exception %s", errno)
    exceptionmap = {
        ERR_NEXIST: NotExistException,
        ERR_INCOMPAT: IncompatibleProtocolVersionException,
        ERR_EXCEPTION: __typ1,
    }
    raise exceptionmap[errno]


def close_socket_thread(ip: <FILL>, port: __typ0) :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(SHUT_WR)
    except socket.timeout:
        s.close()
        raise TimeoutError('ERROR: could not close socket due to timeout')
