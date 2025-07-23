# -*- coding: utf-8 -*-
from typing import Any, Dict

from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'yo'
    URL_TEMPLATE = u"/api/v1/external/yo?api_key={api_key}"
    FIXTURE_DIR_NAME = 'yo'

    def test_yo_message(__tmp0) -> None:
        """
        Yo App sends notification whenever user receives a new Yo from another user.
        """
        __tmp0.url = __tmp0.build_webhook_url(
            email="cordelia@zulip.com",
            username="IAGO",
            user_ip="127.0.0.1"
        )
        expected_message = u"Yo from IAGO"
        __tmp0.send_and_test_private_message('', expected_message=expected_message,
                                           content_type="application/x-www-form-urlencoded")

    def get_body(__tmp0, __tmp1: <FILL>) :
        return {}
