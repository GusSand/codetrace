from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
"""Utilities to help with aiohttp."""
import json
from urllib.parse import parse_qsl
from typing import Any, Dict, Optional

from aiohttp import web
from multidict import CIMultiDict, MultiDict


class __typ0:
    """Mock an aiohttp request."""

    def __tmp2(self, content: <FILL>, method: __typ1 = 'GET',
                 status: int = 200, headers: Optional[Dict[__typ1, __typ1]] = None,
                 query_string: Optional[__typ1] = None, url: __typ1 = '') :
        """Initialize a request."""
        self.method = method
        self.url = url
        self.status = status
        self.headers = CIMultiDict(headers or {})  # type: CIMultiDict[str]
        self.query_string = query_string or ''
        self._content = content

    @property
    def __tmp0(self) -> 'MultiDict[str]':
        """Return a dictionary with the query variables."""
        return MultiDict(parse_qsl(self.query_string, keep_blank_values=True))

    @property
    def _text(self) :
        """Return the body as text."""
        return self._content.decode('utf-8')

    async def json(self) -> __typ2:
        """Return the body as JSON."""
        return json.loads(self._text)

    async def __tmp3(self) :
        """Return POST parameters."""
        return MultiDict(parse_qsl(self._text, keep_blank_values=True))

    async def __tmp1(self) :
        """Return the body as text."""
        return self._text


def serialize_response(response: web.Response) :
    """Serialize an aiohttp response to a dictionary."""
    return {
        'status': response.status,
        'body': response.body,
        'headers': dict(response.headers),
    }
