from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "float"
# See readme.md for instructions on running this code.
import requests
import json
import logging

from typing import Any, Dict

api_url = 'http://api.openweathermap.org/data/2.5/weather'

class __typ2(object):
    def __tmp4(__tmp1, __tmp3: <FILL>) -> None:
        __tmp1.api_key = __tmp3.get_config_info('weather')['key']
        __tmp1.response_pattern = 'Weather in {}, {}:\n{:.2f} F / {:.2f} C\n{}'
        __tmp1.check_api_key(__tmp3)

    def check_api_key(__tmp1, __tmp3) :
        api_params = dict(q='nyc', APPID=__tmp1.api_key)
        test_response = requests.get(api_url, params=api_params)
        try:
            test_response_data = test_response.json()
            if test_response_data['cod'] == 401:
                __tmp3.quit('API Key not valid. Please see doc.md to find out how to get it.')
        except KeyError:
            pass

    def usage(__tmp1) -> __typ1:
        return '''
            This plugin will give info about weather in a specified city
            '''

    def handle_message(__tmp1, __tmp0: Dict[__typ1, __typ1], __tmp3: Any) -> None:
        help_content = '''
            This bot returns weather info for specified city.
            You specify city in the following format:
            city, state/country
            state and country parameter is optional(useful when there are many cities with the same name)
            For example:
            @**Weather Bot** Portland
            @**Weather Bot** Portland, Me
            '''.strip()

        if (__tmp0['content'] == 'help') or (__tmp0['content'] == ''):
            response = help_content
        else:
            api_params = dict(q=__tmp0['content'], APPID=__tmp1.api_key)
            r = requests.get(api_url, params=api_params)
            if r.json()['cod'] == "404":
                response = "Sorry, city not found"
            else:
                response = __tmp5(r, __tmp0['content'], __tmp1.response_pattern)

        __tmp3.send_reply(__tmp0, response)


def __tmp5(__tmp2: Any, __tmp6, response_pattern: __typ1) -> __typ1:
    j = __tmp2.json()
    __tmp6 = j['name']
    country = j['sys']['country']
    fahrenheit = to_fahrenheit(j['main']['temp'])
    celsius = to_celsius(j['main']['temp'])
    description = j['weather'][0]['description'].title()

    return response_pattern.format(__tmp6, country, fahrenheit, celsius, description)


def to_celsius(temp_kelvin) -> __typ0:
    return int(temp_kelvin) - 273.15


def to_fahrenheit(temp_kelvin: __typ0) -> __typ0:
    return int(temp_kelvin) * (9. / 5.) - 459.67

handler_class = __typ2
