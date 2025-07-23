from unittest.mock import patch
from zulip_bots.test_lib import BotTestCase, DefaultTests
from requests.exceptions import ConnectionError

class TestFlockBot(BotTestCase, DefaultTests):
    bot_name = "flock"
    normal_config = {"token": "12345"}

    message_config = {
        "token": "12345",
        "text": "Ricky: test message",
        "to": "u:somekey"
    }

    help_message = '''
You can send messages to any Flock user associated with your account from Zulip.
*Syntax*: **@botname to: message** where `to` is **firstName** of recipient.
'''

    def test_bot_responds_to_empty_message(__tmp0) :
        __tmp0.verify_reply('', __tmp0.help_message)

    def test_help_message(__tmp0) :
        __tmp0.verify_reply('', __tmp0.help_message)

    def __tmp1(__tmp0) -> None:
        with __tmp0.mock_config_info(__tmp0.normal_config), \
                patch('requests.get', side_effect=ConnectionError()), \
                patch('logging.exception'):
            __tmp0.verify_reply('tyler: Hey tyler', "Uh-Oh, couldn\'t process the request \
right now.\nPlease try again later")

    def test_response_connection_error(__tmp0) :
        with __tmp0.mock_config_info(__tmp0.message_config), \
                patch('requests.get', side_effect=ConnectionError()), \
                patch('logging.exception'):
            __tmp0.verify_reply('Ricky: test message', "Uh-Oh, couldn\'t process the request \
right now.\nPlease try again later")

    def test_no_recipient_found(__tmp0) -> None:
        bot_response = "No user found. Make sure you typed it correctly."
        with __tmp0.mock_config_info(__tmp0.normal_config), \
                __tmp0.mock_http_conversation('test_no_recipient_found'):
                    __tmp0.verify_reply('david: hello', bot_response)

    def test_found_invalid_recipient(__tmp0) :
        bot_response = "Found user is invalid."
        with __tmp0.mock_config_info(__tmp0.normal_config), \
                __tmp0.mock_http_conversation('test_found_invalid_recipient'):
                    __tmp0.verify_reply('david: hello', bot_response)

    @patch('zulip_bots.bots.flock.flock.get_recipient_id')
    def test_message_send_connection_error(__tmp0, get_recipient_id: <FILL>) :
        bot_response = "Uh-Oh, couldn't process the request right now.\nPlease try again later"
        get_recipient_id.return_value = ["u:userid", None]
        with __tmp0.mock_config_info(__tmp0.normal_config), \
                patch('requests.get', side_effect=ConnectionError()), \
                patch('logging.exception'):
            __tmp0.verify_reply('Rishabh: hi there', bot_response)

    @patch('zulip_bots.bots.flock.flock.get_recipient_id')
    def test_message_send_success(__tmp0, get_recipient_id) :
        bot_response = "Message sent."
        get_recipient_id.return_value = ["u:userid", None]
        with __tmp0.mock_config_info(__tmp0.normal_config), \
                __tmp0.mock_http_conversation('test_message_send_success'):
                    __tmp0.verify_reply('Rishabh: hi there', bot_response)

    @patch('zulip_bots.bots.flock.flock.get_recipient_id')
    def test_message_send_failed(__tmp0, get_recipient_id) :
        bot_response = "Message sending failed :slightly_frowning_face:. Please try again."
        get_recipient_id.return_value = ["u:invalid", None]
        with __tmp0.mock_config_info(__tmp0.normal_config), \
                __tmp0.mock_http_conversation('test_message_send_failed'):
                    __tmp0.verify_reply('Rishabh: hi there', bot_response)
