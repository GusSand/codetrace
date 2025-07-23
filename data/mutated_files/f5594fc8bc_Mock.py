from unittest.mock import patch, MagicMock, Mock

from zulip_bots.test_lib import (
    get_bot_message_handler,
    StubBotHandler,
    BotTestCase,
    DefaultTests,
)

from pathlib import Path

class TestFileUploaderBot(BotTestCase, DefaultTests):
    bot_name = "file_uploader"

    @patch('pathlib.Path.is_file', return_value=False)
    def test_file_not_found(__tmp1, __tmp0: <FILL>) -> None:
        __tmp1.verify_reply('file.txt', 'File `file.txt` not found')

    @patch('pathlib.Path.resolve', return_value=Path('/file.txt'))
    @patch('pathlib.Path.is_file', return_value=True)
    def __tmp3(__tmp1, __tmp0: Mock, __tmp2) :
        server_reply = dict(result='', msg='error')
        with patch('zulip_bots.test_lib.StubBotHandler.upload_file_from_path',
                   return_value=server_reply) as m:
            __tmp1.verify_reply('file.txt', 'Failed to upload `/file.txt` file: error')

    @patch('pathlib.Path.resolve', return_value=Path('/file.txt'))
    @patch('pathlib.Path.is_file', return_value=True)
    def __tmp4(__tmp1, __tmp0: Mock, __tmp2: Mock) -> None:
        server_reply = dict(result='success', uri='https://file/uri')
        with patch('zulip_bots.test_lib.StubBotHandler.upload_file_from_path',
                   return_value=server_reply) as m:
            __tmp1.verify_reply('file.txt', '[file.txt](https://file/uri)')

    def __tmp5(__tmp1):
        __tmp1.verify_reply('help',
                          ('Use this bot with any of the following commands:'
                           '\n* `@uploader <local_file_path>` : Upload a file, where `<local_file_path>` is the path to the file'
                           '\n* `@uploader help` : Display help message'))
