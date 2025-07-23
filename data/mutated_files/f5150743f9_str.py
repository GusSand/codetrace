from typing import Any, Dict, Optional

from zulip_bots.test_lib import BotTestCase, DefaultTests

class __typ1(BotTestCase, DefaultTests):
    bot_name = 'front'

    def make_request_message(__tmp2, __tmp5: str) :
        message = super().make_request_message(__tmp5)
        message['subject'] = "cnv_kqatm2"
        message['sender_email'] = "leela@planet-express.com"
        return message

    def test_bot_invalid_api_key(__tmp2) -> None:
        invalid_api_key = ''
        with __tmp2.mock_config_info({'api_key': invalid_api_key}):
            with __tmp2.assertRaises(KeyError):
                bot, bot_handler = __tmp2._get_handlers()

    def test_bot_responds_to_empty_message(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            __tmp2.verify_reply("", "Unknown command. Use `help` for instructions.")

    def test_help(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            __tmp2.verify_reply('help', "`archive` Archive a conversation.\n"
                                      "`delete` Delete a conversation.\n"
                                      "`spam` Mark a conversation as spam.\n"
                                      "`open` Restore a conversation.\n"
                                      "`comment <text>` Leave a comment.\n")

    def __tmp7(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('archive'):
                __tmp2.verify_reply('archive', "Conversation was archived.")

    def __tmp0(__tmp2) -> None:
        __tmp2._test_command_error('archive')

    def __tmp3(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('delete'):
                __tmp2.verify_reply('delete', "Conversation was deleted.")

    def test_delete_error(__tmp2) -> None:
        __tmp2._test_command_error('delete')

    def __tmp8(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('spam'):
                __tmp2.verify_reply('spam', "Conversation was marked as spam.")

    def test_spam_error(__tmp2) -> None:
        __tmp2._test_command_error('spam')

    def test_restore(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('open'):
                __tmp2.verify_reply('open', "Conversation was restored.")

    def __tmp6(__tmp2) :
        __tmp2._test_command_error('open')

    def __tmp1(__tmp2) :
        body = "@bender, I thought you were supposed to be cooking for this party."
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('comment'):
                __tmp2.verify_reply("comment " + body, "Comment was sent.")

    def __tmp4(__tmp2) -> None:
        body = "@bender, I thought you were supposed to be cooking for this party."
        __tmp2._test_command_error('comment', body)

    def _test_command_error(__tmp2, command_name: <FILL>, command_arg: Optional[str] = None) -> None:
        bot_command = command_name
        if command_arg:
            bot_command += ' {}'.format(command_arg)
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            with __tmp2.mock_http_conversation('{}_error'.format(command_name)):
                __tmp2.verify_reply(bot_command, 'Something went wrong.')


class __typ0(BotTestCase, DefaultTests):
    bot_name = 'front'

    def make_request_message(__tmp2, __tmp5: str) :
        message = super().make_request_message(__tmp5)
        message['subject'] = "kqatm2"
        return message

    def test_bot_responds_to_empty_message(__tmp2) -> None:
        pass

    def test_no_conversation_id(__tmp2) -> None:
        with __tmp2.mock_config_info({'api_key': "TEST"}):
            __tmp2.verify_reply('archive', "No coversation ID found. Please make "
                                         "sure that the name of the topic "
                                         "contains a valid coversation ID.")
