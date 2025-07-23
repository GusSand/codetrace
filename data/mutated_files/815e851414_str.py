# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'test'
    URL_TEMPLATE = u"/api/v1/external/flock?api_key={api_key}&stream={stream}"

    def __tmp4(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"This is the welcome message!"
        __tmp2.send_and_test_stream_message('messages',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp8(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"It's interesting how high productivity will go..."
        __tmp2.send_and_test_stream_message('reply',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp7(__tmp2) :
        expected_topic = u"Flock notifications"
        expected_message = u"Shared a note"
        __tmp2.send_and_test_stream_message('note',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp3(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"This is reply to Note."
        __tmp2.send_and_test_stream_message('reply_note',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp11(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"This is reply to pinned message."
        __tmp2.send_and_test_stream_message('reply_pinned',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def test_flock_reply_reminder(__tmp2) :
        expected_topic = u"Flock notifications"
        expected_message = u"This is a reply to Reminder."
        __tmp2.send_and_test_stream_message('reply_reminder',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp6(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"This is a reply to Todo notification."
        __tmp2.send_and_test_stream_message('reply_todo',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp0(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"Rishabh rawat pinned an item to the conversation"
        __tmp2.send_and_test_stream_message('pinned',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp9(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"Rishabh rawat wanted me to remind All"
        __tmp2.send_and_test_stream_message('reminder',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp5(__tmp2) -> None:
        expected_topic = u"Flock notifications"
        expected_message = u"Rishabh rawat added a to-do in New List 1 list"
        __tmp2.send_and_test_stream_message('todo',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/json")

    def __tmp1(__tmp2, __tmp10: <FILL>) :
        return __tmp2.webhook_fixture_data("flock", __tmp10, file_type="json")
