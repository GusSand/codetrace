# -*- coding: utf-8 -*-

from zerver.lib.test_classes import WebhookTestCase

# Tests for the Desk.com webhook integration.
#
# The stream name must be provided in the url-encoded test fixture data,
# and must match STREAM_NAME set here.
#
# Example:
#
# stream=deskdotcom&topic=static%20text%20notification&data=This%20is%20a%20custom%20action.
#

class DeskDotComHookTests(WebhookTestCase):
    STREAM_NAME = 'deskdotcom'
    URL_TEMPLATE = "/api/v1/external/deskdotcom?stream={stream}"
    FIXTURE_DIR_NAME = 'deskdotcom'

    def __tmp3(__tmp1) :

        expected_topic = u"static text notification"
        expected_message = u"This is a custom action."

        __tmp1.api_stream_message(__tmp1.TEST_USER_EMAIL, 'static_text', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def __tmp5(__tmp1) :
        expected_topic = u"case updated notification"
        expected_message = (u"Case 2 updated. "
                            u"Link: <a href='https://deskdotcomtest.desk.com/web/agent/case/2'>"
                            u"I have a question</a>")

        __tmp1.api_stream_message(__tmp1.TEST_USER_EMAIL, 'case_updated', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def __tmp2(__tmp1) :

        expected_topic = u"case updated notification"
        expected_message = (u"Case 2 updated. "
                            u"Link: <a href='https://deskdotcomtest.desk.com/web/agent/case/2'>"
                            u"Il mio hovercraft è pieno di anguille.</a>")

        __tmp1.api_stream_message(__tmp1.TEST_USER_EMAIL, 'unicode_text_italian', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def test_unicode_text_japanese(__tmp1) :

        expected_topic = u"case updated notification"
        expected_message = (u"Case 2 updated. "
                            u"Link: <a href='https://deskdotcomtest.desk.com/web/agent/case/2'>"
                            u"私のホバークラフトは鰻でいっぱいです</a>")

        __tmp1.api_stream_message(__tmp1.TEST_USER_EMAIL, 'unicode_text_japanese', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def __tmp0(__tmp1, __tmp4: <FILL>) :
        return __tmp1.webhook_fixture_data("deskdotcom", __tmp4, file_type="txt")
