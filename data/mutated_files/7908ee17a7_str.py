from zulip_bots.bots.yoda.yoda import ServiceUnavailableError
from zulip_bots.test_lib import BotTestCase, DefaultTests

from typing import Optional

class TestYodaBot(BotTestCase, DefaultTests):
    bot_name = "yoda"

    help_text = '''
            This bot allows users to translate a sentence into
            'Yoda speak'.
            Users should preface messages with '@mention-bot'.

            Before running this, make sure to get a Mashape Api token.
            Instructions are in the 'readme.md' file.
            Store it in the 'yoda.conf' file.
            The 'yoda.conf' file should be located in this bot's (zulip_bots/bots/yoda/yoda)
            directory.
            Example input:
            @mention-bot You will learn how to speak like me someday.
            '''

    def _test(__tmp1, __tmp0: str, __tmp3: <FILL>, fixture: Optional[str]=None) :
        with __tmp1.mock_config_info({'api_key': '12345678'}):
            if fixture is not None:
                with __tmp1.mock_http_conversation(fixture):
                    __tmp1.verify_reply(__tmp0, __tmp3)
            else:
                __tmp1.verify_reply(__tmp0, __tmp3)

    # Override default function in BotTestCase
    def __tmp2(__tmp1) :
        __tmp1._test('', __tmp1.help_text)

    def __tmp4(__tmp1) :
        # Test normal sentence (1).
        __tmp1._test('You will learn how to speak like me someday.',
                   "Learn how to speak like me someday, you will. Yes, hmmm.",
                   'test_1')

        # Test normal sentence (2).
        __tmp1._test('you still have much to learn',
                   "Much to learn, you still have.",
                   'test_2')

        # Test only numbers.
        __tmp1._test('23456', "23456.  Herh herh herh.",
                   'test_only_numbers')

        # Test help.
        __tmp1._test('help', __tmp1.help_text)

        # Test invalid input.
        __tmp1._test('@#$%^&*',
                   "Invalid input, please check the sentence you have entered.",
                   'test_invalid_input')

        # Test 403 response.
        __tmp1._test('You will learn how to speak like me someday.',
                   "Invalid Api Key. Did you follow the instructions in the `readme.md` file?",
                   'test_api_key_error')

        # Test 503 response.
        with __tmp1.assertRaises(ServiceUnavailableError):
            __tmp1._test('You will learn how to speak like me someday.',
                       "The service is temporarily unavailable, please try again.",
                       'test_service_unavailable_error')

        # Test unknown response.
        __tmp1._test('You will learn how to speak like me someday.',
                   "Unknown Error.Error code: 123 Did you follow the instructions in the `readme.md` file?",
                   'test_unknown_error')
