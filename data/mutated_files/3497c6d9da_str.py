# -*- coding: utf-8 -*-

from zerver.lib.test_classes import WebhookTestCase


class __typ0(WebhookTestCase):
    STREAM_NAME = 'test'
    URL_TEMPLATE = "/api/v1/external/insping?&api_key={api_key}&stream={stream}"
    FIXTURE_DIR_NAME = 'insping'

    def test_website_state_available_message(__tmp0) :
        expected_topic = u"insping"
        expected_message = u"State changed: Available\n" \
                           u"URL: http://privisus.zulipdev.org:9991\n" \
                           u"Response time: 223 ms\n" \
                           u"Timestamp: Fri Dec 29 17:23:46 2017"

        __tmp0.send_and_test_stream_message('website_state_available',
                                          expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_website_state_not_responding_message(__tmp0) :
        expected_topic = u"insping"
        expected_message = u"State changed: Not Responding\n" \
                           u"URL: http://privisus.zulipdev.org:9991\n" \
                           u"Response time: 942 ms\n" \
                           u"Timestamp: Fri Dec 29 17:13:46 2017"

        __tmp0.send_and_test_stream_message('website_state_not_responding',
                                          expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def get_body(__tmp0, fixture_name: <FILL>) -> str:
        return __tmp0.webhook_fixture_data("insping", fixture_name, file_type="json")
