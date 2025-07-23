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

    def __tmp4(__tmp2) -> None:
        __tmp2.verify_reply('', __tmp2.help_message)

    def test_help_message(__tmp2) -> None:
        __tmp2.verify_reply('', __tmp2.help_message)

    def __tmp6(__tmp2) :
        with __tmp2.mock_config_info(__tmp2.normal_config), \
                patch('requests.get', side_effect=ConnectionError()), \
                patch('logging.exception'):
            __tmp2.verify_reply('tyler: Hey tyler', "Uh-Oh, couldn\'t process the request \
right now.\nPlease try again later")

    def __tmp0(__tmp2) -> None:
        with __tmp2.mock_config_info(__tmp2.message_config), \
                patch('requests.get', side_effect=ConnectionError()), \
                patch('logging.exception'):
            __tmp2.verify_reply('Ricky: test message', "Uh-Oh, couldn\'t process the request \
right now.\nPlease try again later")

    def __tmp3(__tmp2) -> None:
        bot_response = "No user found. Make sure you typed it correctly."
        with __tmp2.mock_config_info(__tmp2.normal_config), \
                __tmp2.mock_http_conversation('test_no_recipient_found'):
                    __tmp2.verify_reply('david: hello', bot_response)

    def __tmp1(__tmp2) :
        bot_response = "Found user is invalid."
        with __tmp2.mock_config_info(__tmp2.normal_config), \
                __tmp2.mock_http_conversation('test_found_invalid_recipient'):
                    __tmp2.verify_reply('david: hello', bot_response)

    @patch('zulip_bots.bots.flock.flock.get_recipient_id')
    def test_message_send_connection_error(__tmp2, __tmp7: str) :
        bot_response = "Uh-Oh, couldn't process the request right now.\nPlease try again later"
        __tmp7.return_value = ["u:userid", None]
        with __tmp2.mock_config_info(__tmp2.normal_config), \
                patch('requests.get', side_effect=ConnectionError()), \
                patch('logging.exception'):
            __tmp2.verify_reply('Rishabh: hi there', bot_response)

    @patch('zulip_bots.bots.flock.flock.get_recipient_id')
    def __tmp5(__tmp2, __tmp7: str) :
        bot_response = "Message sent."
        __tmp7.return_value = ["u:userid", None]
        with __tmp2.mock_config_info(__tmp2.normal_config), \
                __tmp2.mock_http_conversation('test_message_send_success'):
                    __tmp2.verify_reply('Rishabh: hi there', bot_response)

    @patch('zulip_bots.bots.flock.flock.get_recipient_id')
    def test_message_send_failed(__tmp2, __tmp7: <FILL>) -> None:
        bot_response = "Message sending failed :slightly_frowning_face:. Please try again."
        __tmp7.return_value = ["u:invalid", None]
        with __tmp2.mock_config_info(__tmp2.normal_config), \
                __tmp2.mock_http_conversation('test_message_send_failed'):
                    __tmp2.verify_reply('Rishabh: hi there', bot_response)
