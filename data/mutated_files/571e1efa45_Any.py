from typing import TypeAlias
__typ1 : TypeAlias = "bool"
import re
import requests
import logging

from typing import Any, Dict

class __typ0(object):
    '''A Zulip bot that will shorten URLs ("links") in a conversation using the
    goo.gl URL shortener.
    '''

    def __tmp5(__tmp0) :
        return (
            'Mention the link shortener bot in a conversation and then enter '
            'any URLs you want to shorten in the body of the message. \n\n'
            '`key` must be set in `link_shortener.conf`.')

    def __tmp3(__tmp0, __tmp1) :
        __tmp0.config_info = __tmp1.get_config_info('link_shortener')
        __tmp0.check_api_key(__tmp1)

    def check_api_key(__tmp0, __tmp1) :
        test_request_data = __tmp0.call_link_shorten_service('www.youtube.com/watch')  # type: Any
        try:
            if __tmp0.is_invalid_token_error(test_request_data):
                __tmp1.quit('Invalid key. Follow the instructions in doc.md for setting API key.')
        except KeyError:
            pass

    def is_invalid_token_error(__tmp0, __tmp2) :
        return __tmp2['status_code'] == 500 and __tmp2['status_txt'] == 'INVALID_ARG_ACCESS_TOKEN'

    def handle_message(__tmp0, message, __tmp1) :
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

        content = message['content']

        if content.strip() == 'help':
            __tmp1.send_reply(
                message,
                HELP_STR
            )
            return

        link_matches = re.findall(REGEX_STR, content)

        shortened_links = [__tmp0.shorten_link(link) for link in link_matches]
        link_pairs = [
            (link_match + ': ' + shortened_link)
            for link_match, shortened_link
            in zip(link_matches, shortened_links)
            if shortened_link != ''
        ]
        final_response = '\n'.join(link_pairs)

        if final_response == '':
            __tmp1.send_reply(
                message,
                'No links found. ' + HELP_STR
            )
            return

        __tmp1.send_reply(message, final_response)

    def shorten_link(__tmp0, __tmp4) :
        '''Shortens a link using goo.gl Link Shortener and returns it, or
        returns an empty string if something goes wrong.

        Parameters:
            long_url (str): The original URL to shorten.
        '''

        __tmp2 = __tmp0.call_link_shorten_service(__tmp4)
        if __tmp2['status_code'] == 200 and __tmp0.has_shorten_url(__tmp2):
            shorten_url = __tmp0.get_shorten_url(__tmp2)
        else:
            shorten_url = ''
        return shorten_url

    def call_link_shorten_service(__tmp0, __tmp4) :
        response = requests.get(
            'https://api-ssl.bitly.com/v3/shorten',
            params={'access_token': __tmp0.config_info['key'], 'longUrl': __tmp4}
        )
        return response.json()

    def has_shorten_url(__tmp0, __tmp2) :
        return 'data' in __tmp2 and 'url' in __tmp2['data']

    def get_shorten_url(__tmp0, __tmp2: <FILL>) :
        return __tmp2['data']['url']

handler_class = __typ0
