# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional

from zerver.lib.test_classes import WebhookTestCase

class ZenDeskHookTests(WebhookTestCase):
    STREAM_NAME = 'zendesk'
    URL_TEMPLATE = u"/api/v1/external/zendesk?stream={stream}"

    DEFAULT_TICKET_TITLE = 'User can\'t login'
    TICKET_TITLE = DEFAULT_TICKET_TITLE

    DEFAULT_TICKET_ID = 54
    TICKET_ID = DEFAULT_TICKET_ID

    DEFAULT_MESSAGE = 'Message'
    MESSAGE = DEFAULT_MESSAGE

    def get_body(__tmp0, fixture_name: <FILL>) :
        return {
            'ticket_title': __tmp0.TICKET_TITLE,
            'ticket_id': __tmp0.TICKET_ID,
            'message': __tmp0.MESSAGE,
            'stream': __tmp0.STREAM_NAME,
        }

    def do_test(__tmp0, expected_topic: Optional[str]=None, expected_message: Optional[str]=None) -> None:
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, "", expected_topic, expected_message,
                                content_type=None)
        __tmp0.TICKET_TITLE = __tmp0.DEFAULT_TICKET_TITLE
        __tmp0.TICKET_ID = __tmp0.DEFAULT_TICKET_ID
        __tmp0.MESSAGE = __tmp0.DEFAULT_MESSAGE

    def test_subject(__tmp0) :
        __tmp0.TICKET_ID = 4
        __tmp0.TICKET_TITLE = "Test ticket"
        __tmp0.do_test(expected_topic='#4: Test ticket')

    def test_long_subject(__tmp0) :
        __tmp0.TICKET_ID = 4
        __tmp0.TICKET_TITLE = "Test ticket" + '!' * 80
        __tmp0.do_test(expected_topic='#4: Test ticket' + '!' * 42 + '...')

    def test_content(__tmp0) :
        __tmp0.MESSAGE = 'New comment:\n> It is better\n* here'
        __tmp0.do_test(expected_message='New comment:\n> It is better\n* here')
