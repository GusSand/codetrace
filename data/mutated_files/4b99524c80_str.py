from typing import TypeAlias
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
# -*- coding: utf-8 -*-

from typing import Any

import django
import mock
from django.test import TestCase
from django.utils import translation
from django.conf import settings
from django.http import HttpResponse
from http.cookies import SimpleCookie

from zerver.lib.test_classes import (
    ZulipTestCase,
)
from zerver.management.commands import makemessages


class __typ2(ZulipTestCase):
    """
    Tranlations strings should change with locale. URLs should be locale
    aware.
    """

    def tearDown(__tmp1) :
        translation.activate(settings.LANGUAGE_CODE)

    # e.g. self.client_post(url) if method is "post"
    def fetch(__tmp1, __tmp5: <FILL>, __tmp4, __tmp8, **kwargs) -> HttpResponse:
        response = getattr(__tmp1.client, __tmp5)(__tmp4, **kwargs)
        __tmp1.assertEqual(response.status_code, __tmp8,
                         msg="Expected %d, received %d for %s to %s" % (
                             __tmp8, response.status_code, __tmp5, __tmp4))
        return response

    def __tmp7(__tmp1) :
        languages = [('en', u'Sign up'),
                     ('de', u'Registrieren'),
                     ('sr', u'Упишите се'),
                     ('zh-hans', u'注册'),
                     ]

        for lang, word in languages:
            response = __tmp1.fetch('get', '/integrations/', 200,
                                  HTTP_ACCEPT_LANGUAGE=lang)
            __tmp1.assert_in_response(word, response)

    def test_cookie(__tmp1) :
        languages = [('en', u'Sign up'),
                     ('de', u'Registrieren'),
                     ('sr', u'Упишите се'),
                     ('zh-hans', u'注册'),
                     ]

        for lang, word in languages:
            # Applying str function to LANGUAGE_COOKIE_NAME to convert unicode
            # into an ascii otherwise SimpleCookie will raise an exception
            __tmp1.client.cookies = SimpleCookie({str(settings.LANGUAGE_COOKIE_NAME): lang})  # type: ignore # https://github.com/python/typeshed/issues/1476

            response = __tmp1.fetch('get', '/integrations/', 200)
            __tmp1.assert_in_response(word, response)

    def __tmp3(__tmp1) -> None:
        languages = [('en', u'Sign up'),
                     ('de', u'Registrieren'),
                     ('sr', u'Упишите се'),
                     ('zh-hans', u'注册'),
                     ]

        for lang, word in languages:
            response = __tmp1.fetch('get', '/{}/integrations/'.format(lang), 200)
            __tmp1.assert_in_response(word, response)


class __typ0(ZulipTestCase):
    def tearDown(__tmp1) :
        translation.activate(settings.LANGUAGE_CODE)

    @mock.patch('zerver.lib.request._')
    def __tmp2(__tmp1, __tmp0) -> None:
        dummy_value = "this arg is bad: '{var_name}' (translated to German)"
        __tmp0.return_value = dummy_value

        email = __tmp1.example_email('hamlet')
        __tmp1.login(email)
        result = __tmp1.client_post("/json/invites",
                                  HTTP_ACCEPT_LANGUAGE='de')

        expected_error = u"this arg is bad: 'invitee_emails' (translated to German)"
        __tmp1.assert_json_error_contains(result,
                                        expected_error,
                                        status_code=400)

    @mock.patch('zerver.views.auth._')
    def __tmp6(__tmp1, __tmp0: __typ3) :
        dummy_value = "Some other language"
        __tmp0.return_value = dummy_value

        email = __tmp1.example_email('hamlet')
        __tmp1.login(email)
        result = __tmp1.client_get("/de/accounts/login/jwt/")

        __tmp1.assert_json_error_contains(result,
                                        dummy_value,
                                        status_code=400)


class FrontendRegexTestCase(TestCase):
    def test_regexes(__tmp1) :
        command = makemessages.Command()

        data = [
            ('{{#tr context}}english text with __variable__{{/tr}}{{/tr}}',
             'english text with __variable__'),

            ('{{t "english text" }}, "extra"}}',
             'english text'),

            ("{{t 'english text' }}, 'extra'}}",
             'english text'),

            ('i18n.t("english text"), "extra",)',
             'english text'),

            ('i18n.t("english text", context), "extra",)',
             'english text'),

            ("i18n.t('english text'), 'extra',)",
             'english text'),

            ("i18n.t('english text', context), 'extra',)",
             'english text'),
        ]

        for input_text, expected in data:
            result = command.extract_strings(input_text)
            __tmp1.assertEqual(len(result), 1)
            __tmp1.assertEqual(result[0], expected)
