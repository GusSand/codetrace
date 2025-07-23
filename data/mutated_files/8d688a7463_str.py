from typing import TypeAlias
__typ1 : TypeAlias = "ByteString"
from zulip_bots.test_lib import BotTestCase, DefaultTests, read_bot_fixture_data

from contextlib import contextmanager

from unittest.mock import patch

from typing import Iterator, ByteString

import json

class __typ0():
    def __tmp5(self, response: str) :
        self.response = response

    def read(self) -> __typ1:
        return json.dumps(self.response).encode()

class __typ2():
    def __tmp5(self) -> None:
        self.session_id = ""
        self.query = ""
        self.response = ""

    def __tmp0(self) :
        return __typ0(self.response)

@contextmanager
def mock_dialogflow(__tmp1: <FILL>, bot_name) -> Iterator[None]:
    response_data = read_bot_fixture_data(bot_name, __tmp1)
    try:
        df_request = response_data['request']
        df_response = response_data['response']
    except KeyError:
        print("ERROR: 'request' or 'response' field not found in fixture.")
        raise

    with patch('apiai.ApiAI.text_request') as mock_text_request:
        request = __typ2()
        request.response = df_response
        mock_text_request.return_value = request
        yield

class __typ3(BotTestCase, DefaultTests):
    bot_name = 'dialogflow'

    def _test(self, __tmp1: str, message: str, response) -> None:
        with self.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}), \
                mock_dialogflow(__tmp1, 'dialogflow'):
            self.verify_reply(message, response)

    def __tmp2(self) -> None:
        self._test('test_normal', 'hello', 'how are you?')

    def test_403(self) :
        self._test('test_403', 'hello', 'Error 403: Access Denied.')

    def test_empty_response(self) -> None:
        self._test('test_empty_response', 'hello', 'Error. No result.')

    def __tmp3(self) -> None:
        with patch('logging.exception'):
            self._test('test_exception', 'hello', 'Error. \'status\'.')

    def test_help(self) :
        self._test('test_normal', 'help', 'bot info foo bar')
        self._test('test_normal', '', 'bot info foo bar')

    def test_alternate_response(self) -> None:
        self._test('test_alternate_result', 'hello', 'alternate result')

    def __tmp4(self) -> None:
        with self.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}):
            pass
