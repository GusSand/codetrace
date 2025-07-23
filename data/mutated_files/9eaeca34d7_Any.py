from typing import TypeAlias
__typ0 : TypeAlias = "str"
# -*- coding: utf-8 -*-
from unittest.mock import patch
from typing import Any
from zerver.lib.test_classes import WebhookTestCase

class BeeminderHookTests(WebhookTestCase):
    STREAM_NAME = 'beeminder'
    URL_TEMPLATE = u"/api/v1/external/beeminder?api_key={api_key}&stream={stream}"

    @patch('zerver.webhooks.beeminder.view.time.time')
    def __tmp4(__tmp1, __tmp2: <FILL>) :
        __tmp2.return_value = 1517739100  # 5.6 hours from fixture value
        expected_topic = u"beekeeper"
        expected_message = '\n'.join([
            'You are going to derail from goal **gainweight** in **{:0.1f} hours**'.format(5.6),
            ' You need **+2 in 7 days (60)** to avoid derailing',
            ' * Pledge: **0$** :relieved:'
        ])

        __tmp1.send_and_test_stream_message('derail',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    @patch('zerver.webhooks.beeminder.view.time.time')
    def __tmp3(__tmp1, __tmp2: Any) -> None:
        __tmp2.return_value = 1517739100  # 5.6 hours from fixture value
        expected_topic = u"beekeeper"
        expected_message = '\n'.join([
            'You are going to derail from goal **gainweight** in **{:0.1f} hours**'.format(5.6),
            ' You need **+2 in 7 days (60)** to avoid derailing',
            ' * Pledge: **5$** :worried:'
        ])
        __tmp1.send_and_test_stream_message('derail_worried',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp0(__tmp1, __tmp5: __typ0) :
        return __tmp1.webhook_fixture_data("beeminder", __tmp5, file_type="json")
