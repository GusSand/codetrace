from typing import TypeAlias
__typ0 : TypeAlias = "str"
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
    writer: asyncio.StreamWriter, __tmp1,
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


def __tmp0(__tmp5: socket.socket, __tmp1) -> None:
    """
    Syncronous version of send_response, using old style sockets

    :param conn: socket.accept() connection
    :param reponse: Dict[Any, Any] response
    :return: None
    """
    __tmp5.send(bencode.encode(__tmp1))
    __tmp5.shutdown(SHUT_WR)


class SyncrNetworkException(Exception):
    """Base exception for network errors"""
    pass


class NotExistException(SyncrNetworkException):
    """Requested object does not exist"""
    pass


class __typ2(SyncrNetworkException):
    """Version number of the protocol not compatible with request"""
    pass


class __typ1(SyncrNetworkException):
    """Other end experienced an unhandled exception"""
    pass


class __typ3(SyncrNetworkException):
    """No peers found or provided to a request function"""
    pass


def raise_network_error(
    __tmp3: <FILL>,
) -> None:
    """Raises an error based on the errno"""
    logger.debug("Raising exception %s", __tmp3)
    exceptionmap = {
        ERR_NEXIST: NotExistException,
        ERR_INCOMPAT: __typ2,
        ERR_EXCEPTION: __typ1,
    }
    raise exceptionmap[__tmp3]


def __tmp4(ip: __typ0, port) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(SHUT_WR)
    except socket.timeout:
        s.close()
        raise TimeoutError('ERROR: could not close socket due to timeout')
