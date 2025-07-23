from typing import TypeAlias
__typ2 : TypeAlias = "Response"
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
import asyncio
from collections.abc import AsyncIterator
import functools
import logging
from typing import Any, Callable, Optional, AsyncIterator as AsyncIteratorType

from oauthlib import oauth2
import requests
from requests.models import CONTENT_CHUNK_SIZE

from ..exceptions import (
    TokenExpiredError,
    ClientRequestError,
    raise_with_traceback
)
from ..universal_http.async_requests import AsyncBasicRequestsHTTPSender
from . import AsyncHTTPSender, AsyncHTTPPolicy, Response, Request
from .requests import RequestsContext


_LOGGER = logging.getLogger(__name__)


class __typ0(AsyncHTTPSender):
    """Implements a basic Pipeline, that supports universal HTTP lib "requests" driver.
    """

    def __init__(__tmp0, universal_http_requests_driver: Optional[AsyncBasicRequestsHTTPSender]=None) :
        __tmp0.driver = universal_http_requests_driver or AsyncBasicRequestsHTTPSender()

    async def __aenter__(__tmp0) :
        await __tmp0.driver.__aenter__()
        return __tmp0

    async def __aexit__(__tmp0, *exc_details):  # pylint: disable=arguments-differ
        await __tmp0.driver.__aexit__(*exc_details)

    async def __tmp1(__tmp0):
        await __tmp0.__aexit__()

    def build_context(__tmp0):
        # type: () -> RequestsContext
        return RequestsContext(
            session=__tmp0.driver.session,
        )

    async def send(__tmp0, request: <FILL>, **kwargs) :
        """Send request object according to configuration.

        :param Request request: The request object to be sent.
        """
        if request.context is None:  # Should not happen, but make mypy happy and does not hurt
            request.context = __tmp0.build_context()

        if request.context.session is not __tmp0.driver.session:
            kwargs['session'] = request.context.session

        return __typ2(
            request,
            await __tmp0.driver.send(request.http_request, **kwargs)
        )


class __typ1(AsyncHTTPPolicy):
    """Implementation of request-oauthlib except and retry logic.
    """
    def __init__(__tmp0, credentials):
        super(__typ1, __tmp0).__init__()
        __tmp0._creds = credentials

    async def send(__tmp0, request, **kwargs):
        session = request.context.session
        try:
            __tmp0._creds.signed_session(session)
        except TypeError: # Credentials does not support session injection
            _LOGGER.warning("Your credentials class does not support session injection. Performance will not be at the maximum.")
            request.context.session = session = __tmp0._creds.signed_session()

        try:
            try:
                return await __tmp0.next.send(request, **kwargs)
            except (oauth2.rfc6749.errors.InvalidGrantError,
                    oauth2.rfc6749.errors.TokenExpiredError) as err:
                error = "Token expired or is invalid. Attempting to refresh."
                _LOGGER.warning(error)

            try:
                try:
                    __tmp0._creds.refresh_session(session)
                except TypeError: # Credentials does not support session injection
                    _LOGGER.warning("Your credentials class does not support session injection. Performance will not be at the maximum.")
                    request.context.session = session = __tmp0._creds.refresh_session()

                return await __tmp0.next.send(request, **kwargs)
            except (oauth2.rfc6749.errors.InvalidGrantError,
                    oauth2.rfc6749.errors.TokenExpiredError) as err:
                msg = "Token expired or is invalid."
                raise_with_traceback(TokenExpiredError, msg, err)

        except (requests.RequestException,
                oauth2.rfc6749.errors.OAuth2Error) as err:
            msg = "Error occurred in request."
            raise_with_traceback(ClientRequestError, msg, err)

