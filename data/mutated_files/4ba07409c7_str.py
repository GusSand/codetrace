from typing import TypeAlias
__typ0 : TypeAlias = "Any"
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

    def __init__(self) :
        """Raise error because this is singleton.

        Use get_instance() instead.

        :raises RuntimeError: Instanciation is not allowed
        """
        raise RuntimeError("Cannot initialize via Constructor")

    @classmethod
    def get_instance(__tmp1) :
        """Get Redis instance.

        :returns: Instance
        """
        if __tmp1.__singleton_instance is None:
            __tmp1.__singleton_instance = __tmp1.__new__(__tmp1)

        return __tmp1.__singleton_instance

    _client: redis.Redis
    url: str

    def ready(self, url: <FILL>) :
        """Initialize (reset) redis client..

        :param url: Redis URL
        """
        self.url = url
        # Call to untyped function "from_url" of "Redis" in typed context
        self._client = redis.Redis.from_url(self.url)
        return

    def set(self, k, __tmp0: bytes, **kargs: __typ0) :
        """Set key-value pair.

        :param k: Key
        :param v: Value
        :param **kargs: Additional parameters passed to Redis.set method
        :returns: Return from Redis.set
        """
        return self._client.set(k, __tmp0, **kargs)

    def get(self, k) -> Optional[bytes]:
        """Get value of key.

        If key does not eixst or expired, return None.

        :param k: Key
        :returns: Value of k
        """
        ret = self._client.get(k)
        # S101 Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
        assert ret is None or isinstance(ret, bytes)  # noqa: S101
        return ret

    def pttl(self, k) :
        """Get the remaining time to live of a key.

        :param k: Key
        :returns: TTL in millisec
        """
        # Call to untyped function "pttl" in typed context
        return self._client.pttl(k)  # type: ignore
