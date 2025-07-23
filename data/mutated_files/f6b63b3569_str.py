from typing import TypeAlias
__typ1 : TypeAlias = "ByteString"
from zulip_bots.test_lib import BotTestCase, DefaultTests, read_bot_fixture_data

from contextlib import contextmanager

from unittest.mock import patch

from typing import Iterator, ByteString

import json

class __typ0():
    def __tmp6(__tmp1, response: <FILL>) -> None:
        __tmp1.response = response

    def read(__tmp1) :
        return json.dumps(__tmp1.response).encode()

class __typ2():
    def __tmp6(__tmp1) :
        __tmp1.session_id = ""
        __tmp1.query = ""
        __tmp1.response = ""

    def __tmp3(__tmp1) :
        return __typ0(__tmp1.response)

@contextmanager
def __tmp7(__tmp2: str, bot_name: str) -> Iterator[None]:
    response_data = read_bot_fixture_data(bot_name, __tmp2)
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

    def _test(__tmp1, __tmp2, __tmp0, response) :
        with __tmp1.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}), \
                __tmp7(__tmp2, 'dialogflow'):
            __tmp1.verify_reply(__tmp0, response)

    def test_normal(__tmp1) -> None:
        __tmp1._test('test_normal', 'hello', 'how are you?')

    def test_403(__tmp1) :
        __tmp1._test('test_403', 'hello', 'Error 403: Access Denied.')

    def __tmp9(__tmp1) :
        __tmp1._test('test_empty_response', 'hello', 'Error. No result.')

    def test_exception(__tmp1) :
        with patch('logging.exception'):
            __tmp1._test('test_exception', 'hello', 'Error. \'status\'.')

    def __tmp8(__tmp1) :
        __tmp1._test('test_normal', 'help', 'bot info foo bar')
        __tmp1._test('test_normal', '', 'bot info foo bar')

    def __tmp5(__tmp1) :
        __tmp1._test('test_alternate_result', 'hello', 'alternate result')

    def __tmp4(__tmp1) :
        with __tmp1.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}):
            pass
