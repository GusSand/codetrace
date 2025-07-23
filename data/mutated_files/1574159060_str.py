from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "float"
# See readme.md for instructions on running this code.
import requests
import json
import logging

from typing import Any, Dict

api_url = 'http://api.openweathermap.org/data/2.5/weather'

class __typ1(object):
    def __tmp3(__tmp0, __tmp2) :
        __tmp0.api_key = __tmp2.get_config_info('weather')['key']
        __tmp0.response_pattern = 'Weather in {}, {}:\n{:.2f} F / {:.2f} C\n{}'
        __tmp0.check_api_key(__tmp2)

    def check_api_key(__tmp0, __tmp2) :
        api_params = dict(q='nyc', APPID=__tmp0.api_key)
        test_response = requests.get(api_url, params=api_params)
        try:
            test_response_data = test_response.json()
            if test_response_data['cod'] == 401:
                __tmp2.quit('API Key not valid. Please see doc.md to find out how to get it.')
        except KeyError:
            pass

    def __tmp6(__tmp0) -> str:
        return '''
            This plugin will give info about weather in a specified city
            '''

    def __tmp1(__tmp0, message, __tmp2) :
        help_content = '''
            This bot returns weather info for specified city.
            You specify city in the following format:
            city, state/country
            state and country parameter is optional(useful when there are many cities with the same name)
            For example:
            @**Weather Bot** Portland
            @**Weather Bot** Portland, Me
            '''.strip()

        if (message['content'] == 'help') or (message['content'] == ''):
            response = help_content
        else:
            api_params = dict(q=message['content'], APPID=__tmp0.api_key)
            r = requests.get(api_url, params=api_params)
            if r.json()['cod'] == "404":
                response = "Sorry, city not found"
            else:
                response = __tmp7(r, message['content'], __tmp0.response_pattern)

        __tmp2.send_reply(message, response)


def __tmp7(text, city: str, response_pattern: <FILL>) :
    j = text.json()
    city = j['name']
    country = j['sys']['country']
    fahrenheit = __tmp8(j['main']['temp'])
    celsius = __tmp4(j['main']['temp'])
    description = j['weather'][0]['description'].title()

    return response_pattern.format(city, country, fahrenheit, celsius, description)


def __tmp4(__tmp5) -> __typ0:
    return int(__tmp5) - 273.15


def __tmp8(__tmp5) :
    return int(__tmp5) * (9. / 5.) - 459.67

handler_class = __typ1
