from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
__typ1 : TypeAlias = "Any"
"""Redis."""

from __future__ import annotations

from typing import Any, ClassVar, Optional, Union, cast
from urllib.parse import urlparse

import redis


# TODO: Use costum storage system?
# https://docs.djangoproject.com/en/2.2/howto/custom-file-storage/
class Redis:
    """Communicate with redis server."""

    __singleton_instance: ClassVar[Optional[Redis]] = None

    def __init__(__tmp1) -> None:
        """Raise error because this is singleton.

        Use get_instance() instead.

        :raises RuntimeError: Instanciation is not allowed
        """
        raise RuntimeError("Cannot initialize via Constructor")

    @classmethod
    def get_instance(cls) -> Redis:
        """Get Redis instance.

        :returns: Instance
        """
        if cls.__singleton_instance is None:
            cls.__singleton_instance = cls.__new__(cls)

        return cls.__singleton_instance

    _client: redis.Redis
    url: str

    def __tmp0(__tmp1, url) -> None:
        """Initialize (reset) redis client..

        :param url: Redis URL
        """
        __tmp1.url = url
        # Call to untyped function "from_url" of "Redis" in typed context
        __tmp1._client = redis.Redis.from_url(__tmp1.url)
        return

    def set(__tmp1, __tmp2: <FILL>, v: __typ0, **kargs: __typ1) :
        """Set key-value pair.

        :param k: Key
        :param v: Value
        :param **kargs: Additional parameters passed to Redis.set method
        :returns: Return from Redis.set
        """
        return __tmp1._client.set(__tmp2, v, **kargs)

    def get(__tmp1, __tmp2: str) -> Optional[__typ0]:
        """Get value of key.

        If key does not eixst or expired, return None.

        :param k: Key
        :returns: Value of k
        """
        ret = __tmp1._client.get(__tmp2)
        # S101 Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
        assert ret is None or isinstance(ret, __typ0)  # noqa: S101
        return ret

    def pttl(__tmp1, __tmp2: str) -> int:
        """Get the remaining time to live of a key.

        :param k: Key
        :returns: TTL in millisec
        """
        # Call to untyped function "pttl" in typed context
        return __tmp1._client.pttl(__tmp2)  # type: ignore
