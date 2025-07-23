# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'slack'
    URL_TEMPLATE = "/api/v1/external/slack?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'slack'

    def test_slack_channel_to_topic(__tmp0) -> None:

        expected_topic = u"channel: general"
        expected_message = u"**slack_user**: `test\n`"
        __tmp0.send_and_test_stream_message('message_info', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_slack_channel_to_stream(__tmp0) :

        __tmp0.STREAM_NAME = 'general'
        __tmp0.url = "{}{}".format(__tmp0.url, "&channels_map_to_topics=0")
        expected_topic = u"Message from Slack"
        expected_message = u"**slack_user**: `test\n`"
        __tmp0.send_and_test_stream_message('message_info', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_missing_data_user_name(__tmp0) -> None:

        payload = __tmp0.get_body('message_info_missing_user_name')
        url = __tmp0.build_webhook_url()
        result = __tmp0.client_post(url, payload, content_type="application/x-www-form-urlencoded")
        __tmp0.assert_json_error(result, "Missing 'user_name' argument")

    def test_missing_data_channel_name(__tmp0) -> None:

        payload = __tmp0.get_body('message_info_missing_channel_name')
        url = __tmp0.build_webhook_url()
        result = __tmp0.client_post(url, payload, content_type="application/x-www-form-urlencoded")
        __tmp0.assert_json_error(result, "Missing 'channel_name' argument")

    def __tmp1(__tmp0) -> None:

        payload = __tmp0.get_body('message_info_missing_text')
        url = __tmp0.build_webhook_url()
        result = __tmp0.client_post(url, payload, content_type="application/x-www-form-urlencoded")
        __tmp0.assert_json_error(result, "Missing 'text' argument")

    def test_invalid_channels_map_to_topics(__tmp0) -> None:

        payload = __tmp0.get_body('message_info')
        url = "{}{}".format(__tmp0.url, "&channels_map_to_topics=abc")
        result = __tmp0.client_post(url, payload, content_type="application/x-www-form-urlencoded")
        __tmp0.assert_json_error(result, 'Error: channels_map_to_topics parameter other than 0 or 1')

    def get_body(__tmp0, fixture_name: <FILL>) :

        return __tmp0.webhook_fixture_data("slack", fixture_name, file_type="txt")
