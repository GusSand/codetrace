# -*- coding: utf-8 -*-
import urllib

from zerver.lib.test_classes import WebhookTestCase
from zerver.models import get_realm, get_user

class __typ0(WebhookTestCase):
    STREAM_NAME = 'gocd'
    URL_TEMPLATE = "/api/v1/external/gocd?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'gocd'
    TOPIC = 'https://github.com/gocd/gocd'

    def test_gocd_message(__tmp1) :
        expected_message = (u"Author: Balaji B <balaji@example.com>\n"
                            u"Build status: Passed :thumbs_up:\n"
                            u"Details: [build log](https://ci.example.com"
                            u"/go/tab/pipeline/history/pipelineName)\n"
                            u"Comment: my hola mundo changes")

        __tmp1.send_and_test_stream_message(
            'pipeline',
            __tmp1.TOPIC,
            expected_message,
            content_type="application/x-www-form-urlencoded"
        )

    def __tmp2(__tmp1) :
        expected_message = (u"Author: User Name <username123@example.com>\n"
                            u"Build status: Failed :thumbs_down:\n"
                            u"Details: [build log](https://ci.example.com"
                            u"/go/tab/pipeline/history/pipelineName)\n"
                            u"Comment: my hola mundo changes")

        __tmp1.send_and_test_stream_message(
            'pipeline_failed',
            __tmp1.TOPIC,
            expected_message,
            content_type="application/x-www-form-urlencoded"
        )

    def __tmp0(__tmp1, fixture_name: <FILL>) :
        return __tmp1.webhook_fixture_data("gocd", fixture_name, file_type="json")
