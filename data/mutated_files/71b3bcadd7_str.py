from zulip_bots.test_lib import BotTestCase, DefaultTests, read_bot_fixture_data

from contextlib import contextmanager

from unittest.mock import patch

from typing import Iterator, ByteString

import json

class MockHttplibRequest():
    def __init__(__tmp0, response: str) :
        __tmp0.response = response

    def read(__tmp0) -> ByteString:
        return json.dumps(__tmp0.response).encode()

class __typ0():
    def __init__(__tmp0) -> None:
        __tmp0.session_id = ""
        __tmp0.query = ""
        __tmp0.response = ""

    def getresponse(__tmp0) -> MockHttplibRequest:
        return MockHttplibRequest(__tmp0.response)

@contextmanager
def mock_dialogflow(test_name: str, bot_name: str) -> Iterator[None]:
    response_data = read_bot_fixture_data(bot_name, test_name)
    try:
        df_request = response_data['request']
        df_response = response_data['response']
    except KeyError:
        print("ERROR: 'request' or 'response' field not found in fixture.")
        raise

    with patch('apiai.ApiAI.text_request') as mock_text_request:
        request = __typ0()
        request.response = df_response
        mock_text_request.return_value = request
        yield

class TestDialogFlowBot(BotTestCase, DefaultTests):
    bot_name = 'dialogflow'

    def _test(__tmp0, test_name: str, message: str, response: <FILL>) -> None:
        with __tmp0.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}), \
                mock_dialogflow(test_name, 'dialogflow'):
            __tmp0.verify_reply(message, response)

    def test_normal(__tmp0) -> None:
        __tmp0._test('test_normal', 'hello', 'how are you?')

    def test_403(__tmp0) -> None:
        __tmp0._test('test_403', 'hello', 'Error 403: Access Denied.')

    def test_empty_response(__tmp0) -> None:
        __tmp0._test('test_empty_response', 'hello', 'Error. No result.')

    def test_exception(__tmp0) -> None:
        with patch('logging.exception'):
            __tmp0._test('test_exception', 'hello', 'Error. \'status\'.')

    def test_help(__tmp0) -> None:
        __tmp0._test('test_normal', 'help', 'bot info foo bar')
        __tmp0._test('test_normal', '', 'bot info foo bar')

    def test_alternate_response(__tmp0) -> None:
        __tmp0._test('test_alternate_result', 'hello', 'alternate result')

    def test_bot_responds_to_empty_message(__tmp0) -> None:
        with __tmp0.mock_config_info({'key': 'abcdefg', 'bot_info': 'bot info foo bar'}):
            pass
