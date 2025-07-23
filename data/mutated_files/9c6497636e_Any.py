from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
import re
import requests
import logging

from typing import Any, Dict

class LinkShortenerHandler(object):
    '''A Zulip bot that will shorten URLs ("links") in a conversation using the
    goo.gl URL shortener.
    '''

    def __tmp4(__tmp0) :
        return (
            'Mention the link shortener bot in a conversation and then enter '
            'any URLs you want to shorten in the body of the message. \n\n'
            '`key` must be set in `link_shortener.conf`.')

    def __tmp2(__tmp0, __tmp1) :
        __tmp0.config_info = __tmp1.get_config_info('link_shortener')
        __tmp0.check_api_key(__tmp1)

    def check_api_key(__tmp0, __tmp1) :
        test_request_data = __tmp0.call_link_shorten_service('www.youtube.com/watch')  # type: Any
        try:
            if __tmp0.is_invalid_token_error(test_request_data):
                __tmp1.quit('Invalid key. Follow the instructions in doc.md for setting API key.')
        except KeyError:
            pass

    def is_invalid_token_error(__tmp0, response_json: Any) -> __typ1:
        return response_json['status_code'] == 500 and response_json['status_txt'] == 'INVALID_ARG_ACCESS_TOKEN'

    def handle_message(__tmp0, message, __tmp1: Any) :
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

    def shorten_link(__tmp0, __tmp3) -> __typ0:
        '''Shortens a link using goo.gl Link Shortener and returns it, or
        returns an empty string if something goes wrong.

        Parameters:
            long_url (str): The original URL to shorten.
        '''

        response_json = __tmp0.call_link_shorten_service(__tmp3)
        if response_json['status_code'] == 200 and __tmp0.has_shorten_url(response_json):
            shorten_url = __tmp0.get_shorten_url(response_json)
        else:
            shorten_url = ''
        return shorten_url

    def call_link_shorten_service(__tmp0, __tmp3) :
        response = requests.get(
            'https://api-ssl.bitly.com/v3/shorten',
            params={'access_token': __tmp0.config_info['key'], 'longUrl': __tmp3}
        )
        return response.json()

    def has_shorten_url(__tmp0, response_json: <FILL>) -> __typ1:
        return 'data' in response_json and 'url' in response_json['data']

    def get_shorten_url(__tmp0, response_json) -> __typ0:
        return response_json['data']['url']

handler_class = LinkShortenerHandler
