from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
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

    def __tmp3(__tmp0) -> None:
        """Raise error because this is singleton.

        Use get_instance() instead.

        :raises RuntimeError: Instanciation is not allowed
        """
        raise RuntimeError("Cannot initialize via Constructor")

    @classmethod
    def get_instance(__tmp2) -> Redis:
        """Get Redis instance.

        :returns: Instance
        """
        if __tmp2.__singleton_instance is None:
            __tmp2.__singleton_instance = __tmp2.__new__(__tmp2)

        return __tmp2.__singleton_instance

    _client: redis.Redis
    url: __typ1

    def __tmp1(__tmp0, url) :
        """Initialize (reset) redis client..

        :param url: Redis URL
        """
        __tmp0.url = url
        # Call to untyped function "from_url" of "Redis" in typed context
        __tmp0._client = redis.Redis.from_url(__tmp0.url)
        return

    def set(__tmp0, __tmp4: __typ1, v: bytes, **kargs: <FILL>) -> Any:
        """Set key-value pair.

        :param k: Key
        :param v: Value
        :param **kargs: Additional parameters passed to Redis.set method
        :returns: Return from Redis.set
        """
        return __tmp0._client.set(__tmp4, v, **kargs)

    def get(__tmp0, __tmp4) -> Optional[bytes]:
        """Get value of key.

        If key does not eixst or expired, return None.

        :param k: Key
        :returns: Value of k
        """
        ret = __tmp0._client.get(__tmp4)
        # S101 Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
        assert ret is None or isinstance(ret, bytes)  # noqa: S101
        return ret

    def pttl(__tmp0, __tmp4: __typ1) :
        """Get the remaining time to live of a key.

        :param k: Key
        :returns: TTL in millisec
        """
        # Call to untyped function "pttl" in typed context
        return __tmp0._client.pttl(__tmp4)  # type: ignore
