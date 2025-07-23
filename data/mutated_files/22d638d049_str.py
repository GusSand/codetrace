from typing import TypeAlias
__typ0 : TypeAlias = "MagicMock"
# -*- coding: utf-8 -*-

from mock import MagicMock, patch

from zerver.lib.test_classes import WebhookTestCase

class GreenhouseHookTests(WebhookTestCase):
    STREAM_NAME = 'greenhouse'
    URL_TEMPLATE = "/api/v1/external/greenhouse?stream={stream}&api_key={api_key}"
    FIXTURE_DIR_NAME = 'greenhouse'
    CONTENT_TYPE = "application/x-www-form-urlencoded"

    def __tmp5(__tmp1) :
        expected_topic = "Hire Candidate - 19"
        expected_message = ("Hire Candidate\n>Johnny Smith\nID: 19"
                            "\nApplying for role:\nDeveloper\n**Emails:**"
                            "\nPersonal\npersonal@example.com\nWork\nwork@example.com\n\n\n>"
                            "**Attachments:**\n[Resume](https://prod-heroku.s3.amazonaws.com/...)")

        __tmp1.send_and_test_stream_message('candidate_hired',
                                          expected_topic,
                                          expected_message,
                                          content_type=__tmp1.CONTENT_TYPE)

    def __tmp4(__tmp1) -> None:
        expected_topic = "Reject Candidate - 265788"
        expected_message = ("Reject Candidate\n>Hector Porter\nID: "
                            "265788\nApplying for role:\nDesigner"
                            "\n**Emails:**\nPersonal\n"
                            "hector.porter.265788@example.com\n\n\n>"
                            "**Attachments:**\n[Resume](https://prod-heroku.s3.amazonaws.com/...)")

        __tmp1.send_and_test_stream_message('candidate_rejected',
                                          expected_topic,
                                          expected_message,
                                          content_type=__tmp1.CONTENT_TYPE)

    def __tmp7(__tmp1) :
        expected_topic = "Candidate Stage Change - 265772"
        expected_message = ("Candidate Stage Change\n>Giuseppe Hurley"
                            "\nID: 265772\nApplying for role:\n"
                            "Designer\n**Emails:**\nPersonal"
                            "\ngiuseppe.hurley@example.com\n\n\n>"
                            "**Attachments:**\n[Resume](https://prod-heroku.s3.amazonaws.com/...)"
                            "\n[Cover_Letter](https://prod-heroku.s3.amazonaws.com/...)"
                            "\n[Attachment](https://prod-heroku.s3.amazonaws.com/...)")

        __tmp1.send_and_test_stream_message('candidate_stage_change',
                                          expected_topic,
                                          expected_message,
                                          content_type=__tmp1.CONTENT_TYPE)

    def __tmp0(__tmp1) :
        expected_topic = "New Prospect Application - 968190"
        expected_message = ("New Prospect Application\n>Trisha Troy"
                            "\nID: 968190\nApplying for role:\n"
                            "Designer\n**Emails:**\nPersonal"
                            "\nt.troy@example.com\n\n\n>**Attachments:**"
                            "\n[Resume](https://prod-heroku.s3.amazonaws.com/...)")

        __tmp1.send_and_test_stream_message('prospect_created',
                                          expected_topic,
                                          expected_message,
                                          content_type=__tmp1.CONTENT_TYPE)

    @patch('zerver.webhooks.greenhouse.view.check_send_webhook_message')
    def __tmp3(
            __tmp1, __tmp2: __typ0) -> None:
        __tmp1.url = __tmp1.build_webhook_url()
        payload = __tmp1.get_body('ping_event')
        result = __tmp1.client_post(__tmp1.url, payload, content_type=__tmp1.CONTENT_TYPE)
        __tmp1.assertFalse(__tmp2.called)
        __tmp1.assert_json_success(result)

    def get_body(__tmp1, __tmp6: <FILL>) -> str:
        return __tmp1.webhook_fixture_data("greenhouse", __tmp6, file_type="json")
