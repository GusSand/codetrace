from typing import TypeAlias
__typ4 : TypeAlias = "HttpResponse"
__typ3 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
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

    def tearDown(__tmp0) :
        translation.activate(settings.LANGUAGE_CODE)

    # e.g. self.client_post(url) if method is "post"
    def fetch(__tmp0, method, url: <FILL>, expected_status: __typ0, **kwargs: __typ3) :
        response = getattr(__tmp0.client, method)(url, **kwargs)
        __tmp0.assertEqual(response.status_code, expected_status,
                         msg="Expected %d, received %d for %s to %s" % (
                             expected_status, response.status_code, method, url))
        return response

    def test_accept_language_header(__tmp0) :
        languages = [('en', u'Sign up'),
                     ('de', u'Registrieren'),
                     ('sr', u'Упишите се'),
                     ('zh-hans', u'注册'),
                     ]

        for lang, word in languages:
            response = __tmp0.fetch('get', '/integrations/', 200,
                                  HTTP_ACCEPT_LANGUAGE=lang)
            __tmp0.assert_in_response(word, response)

    def test_cookie(__tmp0) -> None:
        languages = [('en', u'Sign up'),
                     ('de', u'Registrieren'),
                     ('sr', u'Упишите се'),
                     ('zh-hans', u'注册'),
                     ]

        for lang, word in languages:
            # Applying str function to LANGUAGE_COOKIE_NAME to convert unicode
            # into an ascii otherwise SimpleCookie will raise an exception
            __tmp0.client.cookies = SimpleCookie({str(settings.LANGUAGE_COOKIE_NAME): lang})  # type: ignore # https://github.com/python/typeshed/issues/1476

            response = __tmp0.fetch('get', '/integrations/', 200)
            __tmp0.assert_in_response(word, response)

    def test_i18n_urls(__tmp0) :
        languages = [('en', u'Sign up'),
                     ('de', u'Registrieren'),
                     ('sr', u'Упишите се'),
                     ('zh-hans', u'注册'),
                     ]

        for lang, word in languages:
            response = __tmp0.fetch('get', '/{}/integrations/'.format(lang), 200)
            __tmp0.assert_in_response(word, response)


class __typ5(ZulipTestCase):
    def tearDown(__tmp0) :
        translation.activate(settings.LANGUAGE_CODE)

    @mock.patch('zerver.lib.request._')
    def test_json_error(__tmp0, mock_gettext: __typ3) :
        dummy_value = "this arg is bad: '{var_name}' (translated to German)"
        mock_gettext.return_value = dummy_value

        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)
        result = __tmp0.client_post("/json/invites",
                                  HTTP_ACCEPT_LANGUAGE='de')

        expected_error = u"this arg is bad: 'invitee_emails' (translated to German)"
        __tmp0.assert_json_error_contains(result,
                                        expected_error,
                                        status_code=400)

    @mock.patch('zerver.views.auth._')
    def test_jsonable_error(__tmp0, mock_gettext: __typ3) -> None:
        dummy_value = "Some other language"
        mock_gettext.return_value = dummy_value

        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)
        result = __tmp0.client_get("/de/accounts/login/jwt/")

        __tmp0.assert_json_error_contains(result,
                                        dummy_value,
                                        status_code=400)


class __typ1(TestCase):
    def test_regexes(__tmp0) :
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
            __tmp0.assertEqual(len(result), 1)
            __tmp0.assertEqual(result[0], expected)
