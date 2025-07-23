# -*- coding: utf-8 -*-

from mock import MagicMock, patch

from zerver.lib.test_classes import WebhookTestCase

class FreshdeskHookTests(WebhookTestCase):
    STREAM_NAME = 'freshdesk'
    URL_TEMPLATE = u"/api/v1/external/freshdesk?stream={stream}"

    def __tmp4(__tmp0) -> None:
        """
        Messages are generated on ticket creation through Freshdesk's
        "Dispatch'r" service.
        """
        expected_topic = u"#11: Test ticket subject ☃"
        expected_message = u"""Requester ☃ Bob <requester-bob@example.com> created [ticket #11](http://test1234zzz.freshdesk.com/helpdesk/tickets/11):

~~~ quote
Test ticket description ☃.
~~~

Type: **Incident**
Priority: **High**
Status: **Pending**"""
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, 'ticket_created', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def __tmp2(__tmp0) -> None:
        """
        Messages are generated when a ticket's status changes through
        Freshdesk's "Observer" service.
        """
        expected_topic = u"#11: Test ticket subject ☃"
        expected_message = """Requester Bob <requester-bob@example.com> updated [ticket #11](http://test1234zzz.freshdesk.com/helpdesk/tickets/11):

Status: **Resolved** => **Waiting on Customer**"""
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, 'status_changed', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def __tmp3(__tmp0) -> None:
        """
        A fixture without the requisite keys should raise JsonableError.
        """
        __tmp0.url = __tmp0.build_webhook_url()
        payload = __tmp0.get_body('status_changed_fixture_with_missing_key')
        kwargs = {
            'HTTP_AUTHORIZATION': __tmp0.encode_credentials(__tmp0.TEST_USER_EMAIL),
            'content_type': 'application/x-www-form-urlencoded',
        }
        result = __tmp0.client_post(__tmp0.url, payload, **kwargs)
        __tmp0.assert_json_error(result, 'Missing key triggered_event in JSON')

    def test_priority_change(__tmp0) -> None:
        """
        Messages are generated when a ticket's priority changes through
        Freshdesk's "Observer" service.
        """
        expected_topic = u"#11: Test ticket subject"
        expected_message = """Requester Bob <requester-bob@example.com> updated [ticket #11](http://test1234zzz.freshdesk.com/helpdesk/tickets/11):

Priority: **High** => **Low**"""
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, 'priority_changed', expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    @patch('zerver.lib.webhooks.common.check_send_webhook_message')
    def __tmp5(
            __tmp0, __tmp1) -> None:
        """
        Ignore unknown event payloads.
        """
        __tmp0.url = __tmp0.build_webhook_url()
        payload = __tmp0.get_body('unknown_payload')
        kwargs = {
            'HTTP_AUTHORIZATION': __tmp0.encode_credentials(__tmp0.TEST_USER_EMAIL),
            'content_type': 'application/x-www-form-urlencoded',
        }
        result = __tmp0.client_post(__tmp0.url, payload, **kwargs)
        __tmp0.assertFalse(__tmp1.called)
        __tmp0.assert_json_success(result)

    def note_change(__tmp0, __tmp6: str, note_type: <FILL>) -> None:
        """
        Messages are generated when a note gets added to a ticket through
        Freshdesk's "Observer" service.
        """
        expected_topic = u"#11: Test ticket subject"
        expected_message = """Requester Bob <requester-bob@example.com> added a {} note to [ticket #11](http://test1234zzz.freshdesk.com/helpdesk/tickets/11).""".format(note_type)
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, __tmp6, expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def test_private_note_change(__tmp0) -> None:
        __tmp0.note_change("private_note", "private")

    def test_public_note_change(__tmp0) -> None:
        __tmp0.note_change("public_note", "public")

    def test_inline_image(__tmp0) -> None:
        """
        Freshdesk sends us descriptions as HTML, so we have to make the
        descriptions Zulip markdown-friendly while still doing our best to
        preserve links and images.
        """
        expected_topic = u"#12: Not enough ☃ guinea pigs"
        expected_message = u"Requester \u2603 Bob <requester-bob@example.com> created [ticket #12](http://test1234zzz.freshdesk.com/helpdesk/tickets/12):\n\n~~~ quote\nThere are too many cat pictures on the internet \u2603. We need more guinea pigs. Exhibit 1:\n\n  \n\n\n[guinea_pig.png](http://cdn.freshdesk.com/data/helpdesk/attachments/production/12744808/original/guinea_pig.png)\n~~~\n\nType: **Problem**\nPriority: **Urgent**\nStatus: **Open**"
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, "inline_images", expected_topic, expected_message,
                                content_type="application/x-www-form-urlencoded")

    def get_body(__tmp0, fixture_name: str) -> str:
        return __tmp0.webhook_fixture_data("freshdesk", fixture_name, file_type="json")
