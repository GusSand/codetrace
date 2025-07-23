from typing import TypeAlias
__typ0 : TypeAlias = "str"
import re
import requests
import logging

from typing import Any, Dict

class __typ1(object):
    '''A Zulip bot that will shorten URLs ("links") in a conversation using the
    goo.gl URL shortener.
    '''

    def __tmp7(__tmp1) -> __typ0:
        return (
            'Mention the link shortener bot in a conversation and then enter '
            'any URLs you want to shorten in the body of the message. \n\n'
            '`key` must be set in `link_shortener.conf`.')

    def __tmp5(__tmp1, __tmp3) :
        __tmp1.config_info = __tmp3.get_config_info('link_shortener')
        __tmp1.check_api_key(__tmp3)

    def check_api_key(__tmp1, __tmp3: Any) :
        test_request_data = __tmp1.call_link_shorten_service('www.youtube.com/watch')  # type: Any
        try:
            if __tmp1.is_invalid_token_error(test_request_data):
                __tmp3.quit('Invalid key. Follow the instructions in doc.md for setting API key.')
        except KeyError:
            pass

    def is_invalid_token_error(__tmp1, __tmp4) -> bool:
        return __tmp4['status_code'] == 500 and __tmp4['status_txt'] == 'INVALID_ARG_ACCESS_TOKEN'

    def __tmp2(__tmp1, __tmp0: Dict[__typ0, __typ0], __tmp3: <FILL>) :
        REGEX_STR = (
            '('
            '(?:http|https):\/\/'  # This allows for the HTTP or HTTPS
                                   # protocol.
            '[^"<>\{\}|\\^~[\]` ]+'  # This allows for any character except
                                     # for certain non-URL-safe ones.
            ')'
        )

        HELP_STR = (
            'Mention the link shortener bot in a conversation and '
            'then enter any URLs you want to shorten in the body of '
            'the message.'
        )

        content = __tmp0['content']

        if content.strip() == 'help':
            __tmp3.send_reply(
                __tmp0,
                HELP_STR
            )
            return

        link_matches = re.findall(REGEX_STR, content)

        shortened_links = [__tmp1.shorten_link(link) for link in link_matches]
        link_pairs = [
            (link_match + ': ' + shortened_link)
            for link_match, shortened_link
            in zip(link_matches, shortened_links)
            if shortened_link != ''
        ]
        final_response = '\n'.join(link_pairs)

        if final_response == '':
            __tmp3.send_reply(
                __tmp0,
                'No links found. ' + HELP_STR
            )
            return

        __tmp3.send_reply(__tmp0, final_response)

    def shorten_link(__tmp1, __tmp6: __typ0) :
        '''Shortens a link using goo.gl Link Shortener and returns it, or
        returns an empty string if something goes wrong.

        Parameters:
            long_url (str): The original URL to shorten.
        '''

        __tmp4 = __tmp1.call_link_shorten_service(__tmp6)
        if __tmp4['status_code'] == 200 and __tmp1.has_shorten_url(__tmp4):
            shorten_url = __tmp1.get_shorten_url(__tmp4)
        else:
            shorten_url = ''
        return shorten_url

    def call_link_shorten_service(__tmp1, __tmp6) :
        response = requests.get(
            'https://api-ssl.bitly.com/v3/shorten',
            params={'access_token': __tmp1.config_info['key'], 'longUrl': __tmp6}
        )
        return response.json()

    def has_shorten_url(__tmp1, __tmp4) -> bool:
        return 'data' in __tmp4 and 'url' in __tmp4['data']

    def get_shorten_url(__tmp1, __tmp4) -> __typ0:
        return __tmp4['data']['url']

handler_class = __typ1
