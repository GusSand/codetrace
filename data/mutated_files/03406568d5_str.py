from typing import TypeAlias
__typ2 : TypeAlias = "HttpResponse"
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponse

from zerver.forms import email_is_not_mit_mailing_list

from zerver.lib.rate_limiter import (
    add_ratelimit_rule,
    clear_history,
    remove_ratelimit_rule,
    RateLimitedUser,
)
from zerver.lib.zephyr import compute_mit_user_fullname

from zerver.lib.test_classes import (
    ZulipTestCase,
)

import DNS
import mock
import time

import urllib

class __typ1(ZulipTestCase):
    def __tmp6(__tmp2) -> None:
        with mock.patch('DNS.dnslookup', return_value=[['starnine:*:84233:101:Athena Consulting Exchange User,,,:/mit/starnine:/bin/bash']]):
            __tmp2.assertEqual(compute_mit_user_fullname(__tmp2.mit_email("starnine")), "Athena Consulting Exchange User")
        with mock.patch('DNS.dnslookup', return_value=[['sipbexch:*:87824:101:Exch Sipb,,,:/mit/sipbexch:/bin/athena/bash']]):
            __tmp2.assertEqual(compute_mit_user_fullname("sipbexch@mit.edu"), "Exch Sipb")

    def __tmp9(__tmp2) -> None:
        with mock.patch('DNS.dnslookup', side_effect=DNS.Base.ServerError('DNS query status: NXDOMAIN', 3)):
            __tmp2.assertEqual(compute_mit_user_fullname("1234567890@mit.edu"), "1234567890@mit.edu")
        with mock.patch('DNS.dnslookup', side_effect=DNS.Base.ServerError('DNS query status: NXDOMAIN', 3)):
            __tmp2.assertEqual(compute_mit_user_fullname("ec-discuss@mit.edu"), "ec-discuss@mit.edu")

    def __tmp4(__tmp2) -> None:
        with mock.patch('DNS.dnslookup', side_effect=DNS.Base.ServerError('DNS query status: NXDOMAIN', 3)):
            __tmp2.assertRaises(ValidationError, email_is_not_mit_mailing_list, "1234567890@mit.edu")
        with mock.patch('DNS.dnslookup', side_effect=DNS.Base.ServerError('DNS query status: NXDOMAIN', 3)):
            __tmp2.assertRaises(ValidationError, email_is_not_mit_mailing_list, "ec-discuss@mit.edu")

    def __tmp5(__tmp2) -> None:
        with mock.patch('DNS.dnslookup', return_value=[['POP IMAP.EXCHANGE.MIT.EDU starnine']]):
            email_is_not_mit_mailing_list("sipbexch@mit.edu")

class __typ0(ZulipTestCase):

    def __tmp8(__tmp2) -> None:
        settings.RATE_LIMITING = True
        add_ratelimit_rule(1, 5)

    def __tmp0(__tmp2) :
        settings.RATE_LIMITING = False
        remove_ratelimit_rule(1, 5)

    def send_api_message(__tmp2, email: str, __tmp7: <FILL>) -> __typ2:
        return __tmp2.api_post(email, "/api/v1/messages", {"type": "stream",
                                                         "to": "Verona",
                                                         "client": "test suite",
                                                         "content": __tmp7,
                                                         "topic": "whatever"})

    def test_headers(__tmp2) -> None:
        user = __tmp2.example_user('hamlet')
        email = user.email
        clear_history(RateLimitedUser(user))

        result = __tmp2.send_api_message(email, "some stuff")
        __tmp2.assertTrue('X-RateLimit-Remaining' in result)
        __tmp2.assertTrue('X-RateLimit-Limit' in result)
        __tmp2.assertTrue('X-RateLimit-Reset' in result)

    def __tmp1(__tmp2) :
        user = __tmp2.example_user('hamlet')
        email = user.email
        clear_history(RateLimitedUser(user))
        result = __tmp2.send_api_message(email, "some stuff")
        limit = int(result['X-RateLimit-Remaining'])

        result = __tmp2.send_api_message(email, "some stuff 2")
        newlimit = int(result['X-RateLimit-Remaining'])
        __tmp2.assertEqual(limit, newlimit + 1)

    def __tmp3(__tmp2) -> None:
        user = __tmp2.example_user('cordelia')
        email = user.email
        clear_history(RateLimitedUser(user))

        start_time = time.time()
        for i in range(6):
            with mock.patch('time.time', return_value=(start_time + i * 0.1)):
                result = __tmp2.send_api_message(email, "some stuff %s" % (i,))

        __tmp2.assertEqual(result.status_code, 429)
        json = result.json()
        __tmp2.assertEqual(json.get("result"), "error")
        __tmp2.assertIn("API usage exceeded rate limit", json.get("msg"))
        __tmp2.assertEqual(json.get('retry-after'), 0.5)
        __tmp2.assertTrue('Retry-After' in result)
        __tmp2.assertEqual(result['Retry-After'], '0.5')

        # We actually wait a second here, rather than force-clearing our history,
        # to make sure the rate-limiting code automatically forgives a user
        # after some time has passed.
        with mock.patch('time.time', return_value=(start_time + 1.0)):
            result = __tmp2.send_api_message(email, "Good message")

            __tmp2.assert_json_success(result)
