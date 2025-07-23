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
from typing import Any, Optional

from ..universal_http.aiohttp import AioHTTPSender as _AioHTTPSenderDriver
from . import AsyncHTTPSender, Request, Response

# Matching requests, because why not?
CONTENT_CHUNK_SIZE = 10 * 1024

class AioHTTPSender(AsyncHTTPSender):
    """AioHttp HTTP sender implementation.
    """

    def __tmp2(__tmp1, driver: Optional[_AioHTTPSenderDriver] = None, *, loop=None) -> None:
        __tmp1.driver = driver or _AioHTTPSenderDriver(loop=loop)

    async def __aenter__(__tmp1):
        await __tmp1.driver.__aenter__()

    async def __aexit__(__tmp1, *exc_details):  # pylint: disable=arguments-differ
        await __tmp1.driver.__aexit__(*exc_details)

    def __tmp0(__tmp1) :
        """Allow the sender to build a context that will be passed
        across the pipeline with the request.

        Return type has no constraints. Implementation is not
        required and None by default.
        """
        return None

    async def send(__tmp1, request: Request, **config: <FILL>) -> Response:
        """Send the request using this HTTP sender.
        """
        return Response(
            request,
            await __tmp1.driver.send(request.http_request)
        )
