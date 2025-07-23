from typing import Any, Dict, Optional

from zulip_bots.test_lib import BotTestCase, DefaultTests

class TestFrontBot(BotTestCase, DefaultTests):
    bot_name = 'front'

    def make_request_message(__tmp0, content) :
        message = super().make_request_message(content)
        message['subject'] = "cnv_kqatm2"
        message['sender_email'] = "leela@planet-express.com"
        return message

    def test_bot_invalid_api_key(__tmp0) :
        invalid_api_key = ''
        with __tmp0.mock_config_info({'api_key': invalid_api_key}):
            with __tmp0.assertRaises(KeyError):
                bot, bot_handler = __tmp0._get_handlers()

    def __tmp1(__tmp0) :
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            __tmp0.verify_reply("", "Unknown command. Use `help` for instructions.")

    def test_help(__tmp0) :
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            __tmp0.verify_reply('help', "`archive` Archive a conversation.\n"
                                      "`delete` Delete a conversation.\n"
                                      "`spam` Mark a conversation as spam.\n"
                                      "`open` Restore a conversation.\n"
                                      "`comment <text>` Leave a comment.\n")

    def test_archive(__tmp0) :
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            with __tmp0.mock_http_conversation('archive'):
                __tmp0.verify_reply('archive', "Conversation was archived.")

    def test_archive_error(__tmp0) -> None:
        __tmp0._test_command_error('archive')

    def test_delete(__tmp0) :
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            with __tmp0.mock_http_conversation('delete'):
                __tmp0.verify_reply('delete', "Conversation was deleted.")

    def test_delete_error(__tmp0) :
        __tmp0._test_command_error('delete')

    def test_spam(__tmp0) -> None:
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            with __tmp0.mock_http_conversation('spam'):
                __tmp0.verify_reply('spam', "Conversation was marked as spam.")

    def test_spam_error(__tmp0) -> None:
        __tmp0._test_command_error('spam')

    def test_restore(__tmp0) :
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            with __tmp0.mock_http_conversation('open'):
                __tmp0.verify_reply('open', "Conversation was restored.")

    def test_restore_error(__tmp0) :
        __tmp0._test_command_error('open')

    def test_comment(__tmp0) -> None:
        body = "@bender, I thought you were supposed to be cooking for this party."
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            with __tmp0.mock_http_conversation('comment'):
                __tmp0.verify_reply("comment " + body, "Comment was sent.")

    def __tmp2(__tmp0) -> None:
        body = "@bender, I thought you were supposed to be cooking for this party."
        __tmp0._test_command_error('comment', body)

    def _test_command_error(__tmp0, __tmp3, command_arg: Optional[str] = None) :
        bot_command = __tmp3
        if command_arg:
            bot_command += ' {}'.format(command_arg)
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            with __tmp0.mock_http_conversation('{}_error'.format(__tmp3)):
                __tmp0.verify_reply(bot_command, 'Something went wrong.')


class __typ0(BotTestCase, DefaultTests):
    bot_name = 'front'

    def make_request_message(__tmp0, content: <FILL>) :
        message = super().make_request_message(content)
        message['subject'] = "kqatm2"
        return message

    def __tmp1(__tmp0) :
        pass

    def test_no_conversation_id(__tmp0) -> None:
        with __tmp0.mock_config_info({'api_key': "TEST"}):
            __tmp0.verify_reply('archive', "No coversation ID found. Please make "
                                         "sure that the name of the topic "
                                         "contains a valid coversation ID.")
