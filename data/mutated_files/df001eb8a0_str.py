from typing import Any, Dict, Optional

from zulip_bots.test_lib import BotTestCase, DefaultTests

class TestFrontBot(BotTestCase, DefaultTests):
    bot_name = 'front'

    def make_request_message(__tmp2, __tmp10: <FILL>) :
        message = super().make_request_message(__tmp10)
        message['subject'] = "cnv_kqatm2"
        message['sender_email'] = "leela@planet-express.com"
        return message

    def test_bot_invalid_api_key(__tmp2) -> None:
        invalid_api_key = ''
        with __tmp2.mock_config_info({'api_key': invalid_api_key}):
            with __tmp2.assertRaises(KeyError):
                bot, bot_handler = __tmp2._get_handlers()

    def __tmp8(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            __tmp2.verify_reply("", "Unknown command. Use `help` for instructions.")

    def __tmp14(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            __tmp2.verify_reply('help', "`archive` Archive a conversation.\n"
                                      "`delete` Delete a conversation.\n"
                                      "`spam` Mark a conversation as spam.\n"
                                      "`open` Restore a conversation.\n"
                                      "`comment <text>` Leave a comment.\n")

    def test_archive(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('archive'):
                __tmp2.verify_reply('archive', "Conversation was archived.")

    def __tmp0(__tmp2) :
        __tmp2._test_command_error('archive')

    def __tmp3(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('delete'):
                __tmp2.verify_reply('delete', "Conversation was deleted.")

    def __tmp7(__tmp2) -> None:
        __tmp2._test_command_error('delete')

    def __tmp6(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('spam'):
                __tmp2.verify_reply('spam', "Conversation was marked as spam.")

    def __tmp13(__tmp2) :
        __tmp2._test_command_error('spam')

    def __tmp5(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('open'):
                __tmp2.verify_reply('open', "Conversation was restored.")

    def __tmp11(__tmp2) :
        __tmp2._test_command_error('open')

    def __tmp1(__tmp2) :
        body = "@bender, I thought you were supposed to be cooking for this party."
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('comment'):
                __tmp2.verify_reply("comment " + body, "Comment was sent.")

    def __tmp9(__tmp2) :
        body = "@bender, I thought you were supposed to be cooking for this party."
        __tmp2._test_command_error('comment', body)

    def _test_command_error(__tmp2, __tmp12, command_arg: Optional[str] = None) :
        bot_command = __tmp12
        if command_arg:
            bot_command += ' {}'.format(command_arg)
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('{}_error'.format(__tmp12)):
                __tmp2.verify_reply(bot_command, 'Something went wrong.')


class __typ0(BotTestCase, DefaultTests):
    bot_name = 'front'

    def make_request_message(__tmp2, __tmp10) :
        message = super().make_request_message(__tmp10)
        message['subject'] = "kqatm2"
        return message

    def __tmp8(__tmp2) :
        pass

    def __tmp4(__tmp2) :
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            __tmp2.verify_reply('archive', "No coversation ID found. Please make "
                                         "sure that the name of the topic "
                                         "contains a valid coversation ID.")
