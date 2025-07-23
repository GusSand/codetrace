from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ2 : TypeAlias = "UserProfile"
# -*- coding: utf-8 -*-
from django.http import HttpRequest

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.exceptions import InvalidJSONError, JsonableError
from zerver.lib.test_classes import ZulipTestCase, WebhookTestCase
from zerver.lib.webhooks.common import \
    validate_extract_webhook_http_header, \
    MISSING_EVENT_HEADER_MESSAGE, MissingHTTPEventHeader, \
    INVALID_JSON_MESSAGE
from zerver.models import get_user, get_realm, UserProfile
from zerver.lib.users import get_api_key
from zerver.lib.send_email import FromAddress
from zerver.lib.test_helpers import HostRequestMock


class __typ1(ZulipTestCase):
    def __tmp6(__tmp0) -> None:
        webhook_bot = get_user('webhook-bot@zulip.com', get_realm('zulip'))
        __tmp5 = HostRequestMock()
        __tmp5.META['HTTP_X_CUSTOM_HEADER'] = 'custom_value'
        __tmp5.user = webhook_bot

        header_value = validate_extract_webhook_http_header(__tmp5, 'X_CUSTOM_HEADER',
                                                            'test_webhook')

        __tmp0.assertEqual(header_value, 'custom_value')

    def __tmp7(__tmp0) -> None:
        webhook_bot = get_user('webhook-bot@zulip.com', get_realm('zulip'))
        webhook_bot.last_reminder = None
        notification_bot = __tmp0.notification_bot()
        __tmp5 = HostRequestMock()
        __tmp5.user = webhook_bot
        __tmp5.path = 'some/random/path'

        exception_msg = "Missing the HTTP event header 'X_CUSTOM_HEADER'"
        with __tmp0.assertRaisesRegex(MissingHTTPEventHeader, exception_msg):
            validate_extract_webhook_http_header(__tmp5, 'X_CUSTOM_HEADER',
                                                 'test_webhook')

        msg = __tmp0.get_last_message()
        expected_message = MISSING_EVENT_HEADER_MESSAGE.format(
            bot_name=webhook_bot.full_name,
            request_path=__tmp5.path,
            header_name='X_CUSTOM_HEADER',
            integration_name='test_webhook',
            support_email=FromAddress.SUPPORT
        ).rstrip()
        __tmp0.assertEqual(msg.sender.email, notification_bot.email)
        __tmp0.assertEqual(msg.content, expected_message)

    def __tmp3(__tmp0):
        @api_key_only_webhook_view('ClientName', notify_bot_owner_on_invalid_json=False)
        def __tmp4(__tmp5: __typ0, __tmp2: __typ2) -> None:
            raise InvalidJSONError("Malformed JSON")

        @api_key_only_webhook_view('ClientName', notify_bot_owner_on_invalid_json=True)
        def __tmp8(__tmp5: __typ0, __tmp2: __typ2) -> None:
            raise InvalidJSONError("Malformed JSON")

        webhook_bot_email = 'webhook-bot@zulip.com'
        webhook_bot_realm = get_realm('zulip')
        webhook_bot = get_user(webhook_bot_email, webhook_bot_realm)
        webhook_bot_api_key = get_api_key(webhook_bot)
        __tmp5 = HostRequestMock()
        __tmp5.POST['api_key'] = webhook_bot_api_key
        __tmp5.host = "zulip.testserver"
        expected_msg = INVALID_JSON_MESSAGE.format(webhook_name='ClientName')

        last_message_id = __tmp0.get_last_message().id
        with __tmp0.assertRaisesRegex(JsonableError, "Malformed JSON"):
            __tmp4(__tmp5)  # type: ignore # mypy doesn't seem to apply the decorator

        # First verify that without the setting, it doesn't send a PM to bot owner.
        msg = __tmp0.get_last_message()
        __tmp0.assertEqual(msg.id, last_message_id)
        __tmp0.assertNotEqual(msg.content, expected_msg.strip())

        # Then verify that with the setting, it does send such a message.
        __tmp8(__tmp5)  # type: ignore # mypy doesn't seem to apply the decorator
        msg = __tmp0.get_last_message()
        __tmp0.assertNotEqual(msg.id, last_message_id)
        __tmp0.assertEqual(msg.sender.email, __tmp0.notification_bot().email)
        __tmp0.assertEqual(msg.content, expected_msg.strip())

class __typ3(WebhookTestCase):
    STREAM_NAME = 'groove'
    URL_TEMPLATE = '/api/v1/external/groove?stream={stream}&api_key={api_key}'

    # This tests the validate_extract_webhook_http_header function with
    # an actual webhook, instead of just making a mock
    def __tmp1(__tmp0) -> None:
        __tmp0.subscribe(__tmp0.test_user, __tmp0.STREAM_NAME)
        result = __tmp0.client_post(__tmp0.url, __tmp0.get_body('ticket_state_changed'),
                                  content_type="application/x-www-form-urlencoded")
        __tmp0.assert_json_error(result, "Missing the HTTP event header 'X_GROOVE_EVENT'")

        webhook_bot = get_user('webhook-bot@zulip.com', get_realm('zulip'))
        webhook_bot.last_reminder = None
        notification_bot = __tmp0.notification_bot()
        msg = __tmp0.get_last_message()
        expected_message = MISSING_EVENT_HEADER_MESSAGE.format(
            bot_name=webhook_bot.full_name,
            request_path='/api/v1/external/groove',
            header_name='X_GROOVE_EVENT',
            integration_name='Groove',
            support_email=FromAddress.SUPPORT
        ).rstrip()
        if msg.sender.email != notification_bot.email:  # nocoverage
            # This block seems to fire occasionally; debug output:
            print(msg)
            print(msg.content)
        __tmp0.assertEqual(msg.sender.email, notification_bot.email)
        __tmp0.assertEqual(msg.content, expected_message)

    def get_body(__tmp0, __tmp9: <FILL>) -> str:
        return __tmp0.webhook_fixture_data("groove", __tmp9, file_type="json")
