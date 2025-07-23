from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
__typ1 : TypeAlias = "bool"
# -*- coding: utf-8 -*-


import asyncio

from asyncio import AbstractEventLoop, StreamReader, StreamWriter
from typing import Iterable, Optional, Tuple


_DEFAULT_LIMIT = 2 ** 16


class _MemoryTransport(asyncio.Transport):
    """Direct connection between a StreamWriter and StreamReader."""

    def __init__(__tmp1, __tmp0: <FILL>) :
        super().__init__()
        __tmp1._reader = __tmp0

    def write(__tmp1, data) :
        __tmp1._reader.feed_data(data)

    def writelines(__tmp1, data) :
        for line in data:
            __tmp1._reader.feed_data(line)
            __tmp1._reader.feed_data(b'\n')

    def write_eof(__tmp1) :
        __tmp1._reader.feed_eof()

    def __tmp2(__tmp1) -> __typ1:
        return True

    def is_closing(__tmp1) :
        return False

    def close(__tmp1) :
        __tmp1.write_eof()


def mempipe(loop: Optional[AbstractEventLoop]=None,
            limit: int=None) -> Tuple[StreamReader, StreamWriter]:
    """In-memory pipe, returns a ``(reader, writer)`` pair.

    .. versionadded:: 0.1

    """

    loop = loop or asyncio.get_event_loop()
    limit = limit or _DEFAULT_LIMIT

    __tmp0 = asyncio.StreamReader(loop=loop, limit=limit)  # type: StreamReader
    writer = asyncio.StreamWriter(
        transport=_MemoryTransport(__tmp0),
        protocol=asyncio.StreamReaderProtocol(__tmp0, loop=loop),
        __tmp0=__tmp0,
        loop=loop,
    )  # type: StreamWriter
    return __tmp0, writer
