from zulip_bots.test_lib import BotTestCase, DefaultTests, read_bot_fixture_data

from contextlib import contextmanager

from unittest.mock import patch

from typing import Iterator, ByteString

import json

class __typ0():
    def __tmp4(__tmp1, response: str) -> None:
        __tmp1.response = response

    def read(__tmp1) -> ByteString:
        return json.dumps(__tmp1.response).encode()

class MockTextRequest():
    def __tmp4(__tmp1) :
        __tmp1.session_id = ""
        __tmp1.query = ""
        __tmp1.response = ""

    def __tmp2(__tmp1) -> __typ0:
        return __typ0(__tmp1.response)

@contextmanager
def mock_dialogflow(__tmp3: str, bot_name: str) :
    response_data = read_bot_fixture_data(bot_name, __tmp3)
    try:
        df_request = response_data['request']
        df_response = response_data['response']
    except KeyError:
        print("ERROR: 'request' or 'response' field not found in fixture.")
        raise

    with patch('apiai.ApiAI.text_request') as mock_text_request:
        request = MockTextRequest()
        request.response = df_response
        mock_text_request.return_value = request
        yield

class TestDialogFlowBot(BotTestCase, DefaultTests):
    bot_name = 'dialogflow'

    def _test(__tmp1, __tmp3: <FILL>, __tmp0: str, response) -> None:
        with __tmp1.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}), \
                mock_dialogflow(__tmp3, 'dialogflow'):
            __tmp1.verify_reply(__tmp0, response)

    def test_normal(__tmp1) -> None:
        __tmp1._test('test_normal', 'hello', 'how are you?')

    def __tmp6(__tmp1) -> None:
        __tmp1._test('test_403', 'hello', 'Error 403: Access Denied.')

    def __tmp5(__tmp1) -> None:
        __tmp1._test('test_empty_response', 'hello', 'Error. No result.')

    def test_exception(__tmp1) :
        with patch('logging.exception'):
            __tmp1._test('test_exception', 'hello', 'Error. \'status\'.')

    def test_help(__tmp1) -> None:
        __tmp1._test('test_normal', 'help', 'bot info foo bar')
        __tmp1._test('test_normal', '', 'bot info foo bar')

    def test_alternate_response(__tmp1) :
        __tmp1._test('test_alternate_result', 'hello', 'alternate result')

    def test_bot_responds_to_empty_message(__tmp1) :
        with __tmp1.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}):
            pass
