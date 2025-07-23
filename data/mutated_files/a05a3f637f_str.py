# -*- coding: utf-8 -*-
from django.conf import settings

from zerver.lib.test_classes import WebhookTestCase
from zerver.models import get_system_bot

class __typ0(WebhookTestCase):
    STREAM_NAME = 'test'
    URL_TEMPLATE = "/api/v1/external/helloworld?&api_key={api_key}&stream={stream}"
    PM_URL_TEMPLATE = "/api/v1/external/helloworld?&api_key={api_key}"
    FIXTURE_DIR_NAME = 'hello'

    # Note: Include a test function per each distinct message condition your integration supports
    def test_hello_message(__tmp1) :
        expected_topic = u"Hello World"
        expected_message = u"Hello! I am happy to be here! :smile:\nThe Wikipedia featured article for today is **[Marilyn Monroe](https://en.wikipedia.org/wiki/Marilyn_Monroe)**"

        # use fixture named helloworld_hello
        __tmp1.send_and_test_stream_message('hello', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_goodbye_message(__tmp1) :
        expected_topic = u"Hello World"
        expected_message = u"Hello! I am happy to be here! :smile:\nThe Wikipedia featured article for today is **[Goodbye](https://en.wikipedia.org/wiki/Goodbye)**"

        # use fixture named helloworld_goodbye
        __tmp1.send_and_test_stream_message('goodbye', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp0(__tmp1) :
        # Note that this is really just a test for check_send_webhook_message
        __tmp1.URL_TEMPLATE = __tmp1.PM_URL_TEMPLATE
        __tmp1.url = __tmp1.build_webhook_url()
        expected_message = u"Hello! I am happy to be here! :smile:\nThe Wikipedia featured article for today is **[Goodbye](https://en.wikipedia.org/wiki/Goodbye)**"

        __tmp1.send_and_test_private_message('goodbye', expected_message=expected_message,
                                           content_type="application/x-www-form-urlencoded")

    def test_stream_error_pm_to_bot_owner(__tmp1) :
        # Note taht this is really just a test for check_send_webhook_message
        __tmp1.STREAM_NAME = 'nonexistent'
        __tmp1.url = __tmp1.build_webhook_url()
        notification_bot = get_system_bot(settings.NOTIFICATION_BOT)
        expected_message = "Hi there! We thought you'd like to know that your bot **Zulip Webhook Bot** just tried to send a message to stream `nonexistent`, but that stream does not yet exist. To create it, click the gear in the left-side stream list."
        __tmp1.send_and_test_private_message('goodbye', expected_message=expected_message,
                                           content_type='application/x-www-form-urlencoded',
                                           sender=notification_bot)

    def test_custom_topic(__tmp1) :
        # Note that this is really just a test for check_send_webhook_message
        expected_topic = u"Custom Topic"
        __tmp1.url = __tmp1.build_webhook_url(topic=expected_topic)
        expected_message = u"Hello! I am happy to be here! :smile:\nThe Wikipedia featured article for today is **[Goodbye](https://en.wikipedia.org/wiki/Goodbye)**"

        __tmp1.send_and_test_stream_message('goodbye', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def get_body(__tmp1, fixture_name: <FILL>) :
        return __tmp1.webhook_fixture_data("helloworld", fixture_name, file_type="json")
