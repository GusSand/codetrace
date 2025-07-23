from typing import TypeAlias
__typ2 : TypeAlias = "ClientRequest"
__typ1 : TypeAlias = "AsyncClientResponse"
# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------
from typing import Any, Callable, AsyncIterator, Optional

import aiohttp
from multidict import CIMultiDict

from . import AsyncHTTPSender, ClientRequest, AsyncClientResponse

# Matching requests, because why not?
CONTENT_CHUNK_SIZE = 10 * 1024


class AioHTTPSender(AsyncHTTPSender):
    """AioHttp HTTP sender implementation.
    """

    def __init__(__tmp0, *, loop=None):
        __tmp0._session = aiohttp.ClientSession(loop=loop)

    async def __aenter__(__tmp0):
        await __tmp0._session.__aenter__()
        return __tmp0

    async def __aexit__(__tmp0, *exc_details):  # pylint: disable=arguments-differ
        await __tmp0._session.__aexit__(*exc_details)

    async def send(__tmp0, request, **config: <FILL>) -> __typ1:
        """Send the request using this HTTP sender.

        Will pre-load the body into memory to be available with a sync method.
        pass stream=True to avoid this behavior.
        """
        result = await __tmp0._session.request(
            request.method,
            request.url,
            **config
        )
        response = __typ0(request, result)
        if not config.get("stream", False):
            await response.load_body()
        return response


class __typ0(__typ1):
    def __init__(__tmp0, request: __typ2, aiohttp_response: aiohttp.ClientResponse) :
        super(__typ0, __tmp0).__init__(request, aiohttp_response)
        # https://aiohttp.readthedocs.io/en/stable/client_reference.html#aiohttp.ClientResponse
        __tmp0.status_code = aiohttp_response.status
        __tmp0.headers = CIMultiDict(aiohttp_response.headers)
        __tmp0.reason = aiohttp_response.reason
        __tmp0._body = None

    def body(__tmp0) :
        """Return the whole body as bytes in memory.
        """
        if not __tmp0._body:
            raise ValueError("Body is not available. Call async method load_body, or do your call with stream=False.")
        return __tmp0._body

    async def load_body(__tmp0) -> None:
        """Load in memory the body, so it could be accessible from sync methods."""
        __tmp0._body = await __tmp0.internal_response.read()

    def raise_for_status(__tmp0):
        __tmp0.internal_response.raise_for_status()

    def stream_download(__tmp0, chunk_size: Optional[int] = None, callback: Optional[Callable] = None) -> AsyncIterator[bytes]:
        """Generator for streaming request body data.
        """
        chunk_size = chunk_size or CONTENT_CHUNK_SIZE
        async def __tmp1(resp):
            while True:
                chunk = await resp.content.read(chunk_size)
                if not chunk:
                    break
                callback(chunk, resp)
        return __tmp1(__tmp0.internal_response)
