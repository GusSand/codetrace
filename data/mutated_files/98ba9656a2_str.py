from typing import TypeAlias
__typ1 : TypeAlias = "Response"
__typ0 : TypeAlias = "int"
from typing import Optional
from datetime import datetime
import time
import math

from requests import Response


class Cache:
    def __tmp3(__tmp0):
        """Cache class.

        The cache is designed to respect the caching rules of ESI as to
        not request a page more often than it is updated by the server.

        Args:
            None

        Returns:
            None
        """
        __tmp0.data: dict = {}

    def _get_expiration(__tmp0, headers) :
        """Gets the expiration time of the data from the response headers.

        Args:
            headers: dictionary of headers from ESI

        Returns:
            value of seconds from now the data expires
        """
        expiration_str = headers.get("expires")
        if not expiration_str:
            return 0
        expiration = datetime.strptime(expiration_str, "%a, %d %b %Y %H:%M:%S %Z")
        delta = (expiration - datetime.utcnow()).total_seconds()
        return math.ceil(abs(delta))

    def set(__tmp0, __tmp1) :
        """Adds a response to the cache.

        Args:
            response: response from ESI

        Returns:
            None
        """
        __tmp0.data[__tmp1.url] = SavedEndpoint(
            __tmp1.json(), __tmp0._get_expiration(__tmp1.headers)
        )

    def _check_expiration(__tmp0, url: <FILL>, data: "SavedEndpoint") -> "SavedEndpoint":
        """Checks the expiration time for data for a url.

        If the data has expired, it is deleted from the cache.

        Args:
            url: url to check
            data: page of data for that url

        Returns:
            value of either the passed data or None if it expired
        """
        if data.expires_after < time.time():
            del __tmp0.data[url]
            data = None
        return data

    def __tmp2(__tmp0, url) -> Optional[dict]:
        """Check if data for a url has expired.

        Data is not fetched again if it has expired.

        Args:
            url: url to check expiration on

        Returns:
            value of the data, possibly None
        """
        data = __tmp0.data.get(url)
        if data:
            data = __tmp0._check_expiration(url, data)
        return data.data if data else None

    def __tmp4(__tmp0) :
        """Returns the number of items in the stored data.

        More of a debugging tool, since getting the number of dictionary keys
        isn't a good indicator of how much data is actually here.

        Args:
            None

        Returns:
            value of the number of keys in the data
        """
        return len(__tmp0.data.keys())


class SavedEndpoint:
    def __tmp3(__tmp0, data, expires_in) -> None:
        """SavedEndpoint class.

        A wrapper around a page from ESI that also includes the expiration time
        in seconds and the time after which the wrapped data expires.

        Args:
            data: page data from ESI
            expires_in: number of seconds from now that the data expires

        Returns:
            None
        """
        __tmp0.data = data
        __tmp0.expires_in = expires_in
        __tmp0.expires_after = time.time() + expires_in
