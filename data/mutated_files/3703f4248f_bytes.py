from typing import TypeAlias
__typ0 : TypeAlias = "bool"
# -*- coding: utf-8 -*-


import asyncio

from asyncio import AbstractEventLoop, StreamReader, StreamWriter
from typing import Iterable, Optional, Tuple


_DEFAULT_LIMIT = 2 ** 16


class _MemoryTransport(asyncio.Transport):
    """Direct connection between a StreamWriter and StreamReader."""

    def __init__(__tmp2, reader) -> None:
        super().__init__()
        __tmp2._reader = reader

    def write(__tmp2, data: <FILL>) -> None:
        __tmp2._reader.feed_data(data)

    def __tmp0(__tmp2, data: Iterable[bytes]) -> None:
        for line in data:
            __tmp2._reader.feed_data(line)
            __tmp2._reader.feed_data(b'\n')

    def write_eof(__tmp2) -> None:
        __tmp2._reader.feed_eof()

    def can_write_eof(__tmp2) -> __typ0:
        return True

    def __tmp1(__tmp2) -> __typ0:
        return False

    def close(__tmp2) -> None:
        __tmp2.write_eof()


def mempipe(loop: Optional[AbstractEventLoop]=None,
            limit: int=None) -> Tuple[StreamReader, StreamWriter]:
    """In-memory pipe, returns a ``(reader, writer)`` pair.

    .. versionadded:: 0.1

    """

    loop = loop or asyncio.get_event_loop()
    limit = limit or _DEFAULT_LIMIT

    reader = asyncio.StreamReader(loop=loop, limit=limit)  # type: StreamReader
    writer = asyncio.StreamWriter(
        transport=_MemoryTransport(reader),
        protocol=asyncio.StreamReaderProtocol(reader, loop=loop),
        reader=reader,
        loop=loop,
    )  # type: StreamWriter
    return reader, writer
