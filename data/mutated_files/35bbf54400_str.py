# -*- coding: utf-8 -*-

from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'delighted'
    URL_TEMPLATE = "/api/v1/external/delighted?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'delighted'

    def __tmp0(__tmp1) :
        expected_topic = "Survey Response"
        expected_message = ("Kudos! You have a new promoter.\n"
                            ">Score of 9/10 from charlie_gravis@example.com"
                            "\n>Your service is fast and flawless!")

        __tmp1.send_and_test_stream_message('survey_response_updated_promoter',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_feedback_message_non_promoter(__tmp1) :
        expected_topic = "Survey Response"
        expected_message = ("Great! You have new feedback.\n"
                            ">Score of 5/10 from paul_gravis@example.com"
                            "\n>Your service is slow, but nearly flawless! "
                            "Keep up the good work!")

        __tmp1.send_and_test_stream_message('survey_response_updated_non_promoter',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def get_body(__tmp1, __tmp2: <FILL>) :
        return __tmp1.webhook_fixture_data("delighted", __tmp2, file_type="json")
