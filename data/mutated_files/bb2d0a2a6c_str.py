# -*- coding: utf-8 -*-

from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'newrelic'
    URL_TEMPLATE = u"/api/v1/external/newrelic?stream={stream}&api_key={api_key}"

    def __tmp0(__tmp2) :
        expected_topic = "Apdex score fell below critical level of 0.90"
        expected_message = 'Alert opened on [application name]: \
Apdex score fell below critical level of 0.90\n\
[View alert](https://rpm.newrelc.com/accounts/[account_id]/applications/[application_id]/incidents/[incident_id])'
        __tmp2.send_and_test_stream_message('alert', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp4(__tmp2) :
        expected_topic = 'Test App deploy'
        expected_message = '`1242` deployed by **Zulip Test**\n\
Description sent via curl\n\nChangelog string'
        __tmp2.send_and_test_stream_message('deployment', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp1(__tmp2, __tmp3: <FILL>) -> str:
        return __tmp2.webhook_fixture_data("newrelic", __tmp3, file_type="txt")
