from typing import TypeAlias
__typ2 : TypeAlias = "str"
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


async def __tmp2(
    writer: asyncio.StreamWriter, __tmp1: Dict[Any, Any],
) -> None:
    """
    Sends a response to a connection and then closes writing to that connection

    :param writer: StreamWriter to write to
    :param response: Dict[Any, Any] response
    :return: None
    """
    writer.write(bencode.encode(__tmp1))
    writer.write_eof()
    await writer.drain()


def __tmp0(__tmp4: socket.socket, __tmp1: Dict[Any, Any]) -> None:
    """
    Syncronous version of send_response, using old style sockets

    :param conn: socket.accept() connection
    :param reponse: Dict[Any, Any] response
    :return: None
    """
    __tmp4.send(bencode.encode(__tmp1))
    __tmp4.shutdown(SHUT_WR)


class __typ1(Exception):
    """Base exception for network errors"""
    pass


class __typ3(__typ1):
    """Requested object does not exist"""
    pass


class __typ0(__typ1):
    """Version number of the protocol not compatible with request"""
    pass


class UnhandledExceptionException(__typ1):
    """Other end experienced an unhandled exception"""
    pass


class __typ4(__typ1):
    """No peers found or provided to a request function"""
    pass


def raise_network_error(
    __tmp3: int,
) -> None:
    """Raises an error based on the errno"""
    logger.debug("Raising exception %s", __tmp3)
    exceptionmap = {
        ERR_NEXIST: __typ3,
        ERR_INCOMPAT: __typ0,
        ERR_EXCEPTION: UnhandledExceptionException,
    }
    raise exceptionmap[__tmp3]


def close_socket_thread(ip: __typ2, port: <FILL>) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(SHUT_WR)
    except socket.timeout:
        s.close()
        raise TimeoutError('ERROR: could not close socket due to timeout')
