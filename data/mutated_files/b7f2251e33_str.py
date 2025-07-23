"""Helper functions for sending tracker requests"""
import asyncio
from typing import Any
from typing import Dict

import bencode  # type: ignore

from syncr_backend.util.log_util import get_logger


logger = get_logger(__name__)


async def __tmp2(
    __tmp1, __tmp0: <FILL>, port: int,
) -> Dict[str, Any]:
    """
    Creates a connection with the tracker and sends a given request to the
    tracker and returns the response

    :param port: port where tracker is serving
    :param ip: ip of tracker
    :param request: ['POST'/'GET', node_id|drop_id, data]
    :return: tracker response
    """
    reader, writer = await asyncio.open_connection(__tmp0, port)

    writer.write(bencode.encode(__tmp1))
    writer.write_eof()
    await writer.drain()

    response = b''
    while 1:
        data = await reader.read()
        if not data:
            break
        else:
            response += data

    reader.feed_eof()

    return bencode.decode(response)
