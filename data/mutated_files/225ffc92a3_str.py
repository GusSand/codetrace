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


async def __tmp4(
    __tmp0, __tmp2: Dict[Any, Any],
) -> None:
    """
    Sends a response to a connection and then closes writing to that connection

    :param writer: StreamWriter to write to
    :param response: Dict[Any, Any] response
    :return: None
    """
    __tmp0.write(bencode.encode(__tmp2))
    __tmp0.write_eof()
    await __tmp0.drain()


def __tmp1(__tmp8: socket.socket, __tmp2: Dict[Any, Any]) :
    """
    Syncronous version of send_response, using old style sockets

    :param conn: socket.accept() connection
    :param reponse: Dict[Any, Any] response
    :return: None
    """
    __tmp8.send(bencode.encode(__tmp2))
    __tmp8.shutdown(SHUT_WR)


class __typ1(Exception):
    """Base exception for network errors"""
    pass


class __typ3(__typ1):
    """Requested object does not exist"""
    pass


class __typ2(__typ1):
    """Version number of the protocol not compatible with request"""
    pass


class UnhandledExceptionException(__typ1):
    """Other end experienced an unhandled exception"""
    pass


class __typ4(__typ1):
    """No peers found or provided to a request function"""
    pass


def __tmp3(
    __tmp6: __typ0,
) -> None:
    """Raises an error based on the errno"""
    logger.debug("Raising exception %s", __tmp6)
    exceptionmap = {
        ERR_NEXIST: __typ3,
        ERR_INCOMPAT: __typ2,
        ERR_EXCEPTION: UnhandledExceptionException,
    }
    raise exceptionmap[__tmp6]


def __tmp7(__tmp5: <FILL>, port: __typ0) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((__tmp5, port))
        s.shutdown(SHUT_WR)
    except socket.timeout:
        s.close()
        raise TimeoutError('ERROR: could not close socket due to timeout')
