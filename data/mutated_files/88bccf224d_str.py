from unittest.mock import patch
from zulip_bots.test_lib import BotTestCase, DefaultTests

from typing import Optional

class __typ0(BotTestCase, DefaultTests):
    bot_name = "weather"

    help_content = '''
            This bot returns weather info for specified city.
            You specify city in the following format:
            city, state/country
            state and country parameter is optional(useful when there are many cities with the same name)
            For example:
            @**Weather Bot** Portland
            @**Weather Bot** Portland, Me
            '''.strip()

    def _test(__tmp1, __tmp0: str, __tmp3: <FILL>, fixture: Optional[str]=None) :
        with __tmp1.mock_config_info({'key': '123456'}):
            if fixture:
                with __tmp1.mock_http_conversation(fixture):
                    __tmp1.verify_reply(__tmp0, __tmp3)
            else:
                __tmp1.verify_reply(__tmp0, __tmp3)

    # Override default function in BotTestCase
    def __tmp2(__tmp1) -> None:
        with patch('requests.get'):
            __tmp1._test('', __tmp1.help_content)

    def __tmp4(__tmp1) :

        # City query
        bot_response = "Weather in New York, US:\n71.33 F / 21.85 C\nMist"
        __tmp1._test('New York', bot_response, 'test_only_city')

        # City with country query
        bot_response = "Weather in New Delhi, IN:\n80.33 F / 26.85 C\nMist"
        __tmp1._test('New Delhi, India', bot_response, 'test_city_with_country')

        # Only country query: returns the weather of the capital city
        bot_response = "Weather in London, GB:\n58.73 F / 14.85 C\nShower Rain"
        __tmp1._test('United Kingdom', bot_response, 'test_only_country')

        # City not found query
        bot_response = "Sorry, city not found"
        __tmp1._test('fghjklasdfgh', bot_response, 'test_city_not_found')

        # help message
        with patch('requests.get'):
            __tmp1._test('help', __tmp1.help_content)
