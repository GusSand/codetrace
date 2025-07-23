from unittest.mock import patch
from zulip_bots.test_lib import BotTestCase, DefaultTests
from zulip_bots.test_lib import StubBotHandler
from zulip_bots.bots.link_shortener.link_shortener import LinkShortenerHandler


class __typ0(BotTestCase, DefaultTests):
    bot_name = "link_shortener"

    def _test(__tmp0, message: <FILL>, response) :
        with __tmp0.mock_config_info({'key': 'qwertyuiop'}):
            __tmp0.verify_reply(message, response)

    def __tmp1(__tmp0) :
        with patch('requests.get'):
            __tmp0._test('',
                       ('No links found. '
                        'Mention the link shortener bot in a conversation and '
                        'then enter any URLs you want to shorten in the body of '
                        'the message.'))

    def test_normal(__tmp0) :
        with __tmp0.mock_http_conversation('test_normal'):
            __tmp0._test('Shorten https://www.github.com/zulip/zulip please.',
                       'https://www.github.com/zulip/zulip: http://bit.ly/2Ht2hOI')

    def __tmp3(__tmp0) -> None:
        # No `mock_http_conversation` is necessary because the bot will
        # recognize that no links are in the message and won't make any HTTP
        # requests.
        with patch('requests.get'):
            __tmp0._test('Shorten nothing please.',
                       ('No links found. '
                        'Mention the link shortener bot in a conversation and '
                        'then enter any URLs you want to shorten in the body of '
                        'the message.'))

    def __tmp4(__tmp0) -> None:
        # No `mock_http_conversation` is necessary because the bot will
        # recognize that the message is 'help' and won't make any HTTP
        # requests.
        with patch('requests.get'):
            __tmp0._test('help',
                       ('Mention the link shortener bot in a conversation and then '
                        'enter any URLs you want to shorten in the body of the message.'))

    def __tmp2(__tmp0)-> None:
        bot_test_instance = LinkShortenerHandler()
        with __tmp0.mock_config_info({'key': 'qwertyuiopx'}):
            with __tmp0.mock_http_conversation('test_invalid_access_token'):
                with __tmp0.assertRaises(StubBotHandler.BotQuitException):
                    bot_test_instance.initialize(StubBotHandler())
