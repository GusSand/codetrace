# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    URL_TEMPLATE = u"/api/v1/external/dialogflow?api_key={api_key}&email=AARON@zulip.com"

    def test_dialogflow_default(__tmp1) :
        __tmp1.url = __tmp1.build_webhook_url(
            email="AARON@zulip.com",
            username="aaron",
            user_ip="127.0.0.1"
        )
        expected_message = u"Today the weather in Delhi: Sunny, And the tempreture is 65F"
        __tmp1.send_and_test_private_message('default',
                                           expected_message,
                                           content_type="application/json")

    def __tmp2(__tmp1) -> None:
        __tmp1.url = __tmp1.build_webhook_url(
            email="AARON@zulip.com",
            username="aaron",
            user_ip="127.0.0.1"
        )
        expected_message = u"The weather sure looks great !"
        __tmp1.send_and_test_private_message('weather_app',
                                           expected_message,
                                           content_type="application/json")

    def test_dialogflow_alternate_result(__tmp1) -> None:
        __tmp1.url = __tmp1.build_webhook_url(
            email="AARON@zulip.com",
            username="aaron",
            user_ip="127.0.0.1"
        )
        expected_message = u"Weather in New Delhi is nice!"
        __tmp1.send_and_test_private_message('alternate_result',
                                           expected_message,
                                           content_type="application/json")

    def test_dialogflow_error_status(__tmp1) :
        __tmp1.url = __tmp1.build_webhook_url(
            email="AARON@zulip.com",
            username="aaron",
            user_ip="127.0.0.1"
        )
        expected_message = u"403 - Access Denied"
        __tmp1.send_and_test_private_message('error_status',
                                           expected_message,
                                           content_type="application/json")

    def __tmp0(__tmp1) :
        __tmp1.url = __tmp1.build_webhook_url(
            email="AARON@zulip.com",
            username="aaron",
            user_ip="127.0.0.1"
        )
        expected_message = u"DialogFlow couldn't process your query."
        __tmp1.send_and_test_private_message('exception',
                                           expected_message,
                                           content_type="application/json")

    def __tmp3(__tmp1, fixture_name: <FILL>) :
        return __tmp1.webhook_fixture_data("dialogflow",
                                         fixture_name,
                                         file_type="json")
