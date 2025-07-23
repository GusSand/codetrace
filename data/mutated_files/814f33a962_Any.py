from typing import Dict, Any, Union
import requests
import logging
from requests.exceptions import HTTPError, ConnectionError

from zulip_bots.custom_exceptions import ConfigValidationError

GIPHY_TRANSLATE_API = 'http://api.giphy.com/v1/gifs/translate'
GIPHY_RANDOM_API = 'http://api.giphy.com/v1/gifs/random'


class __typ1(object):
    """
    This plugin posts a GIF in response to the keywords provided by the user.
    Images are provided by Giphy, through the public API.
    The bot looks for messages starting with @mention of the bot
    and responds with a message with the GIF based on provided keywords.
    It also responds to private messages.
    """
    def usage(self) -> str:
        return '''
            This plugin allows users to post GIFs provided by Giphy.
            Users should preface keywords with the Giphy-bot @mention.
            The bot responds also to private messages.
            '''

    @staticmethod
    def validate_config(config_info: Dict[str, str]) -> None:
        query = {'s': 'Hello',
                 'api_key': config_info['key']}
        try:
            data = requests.get(GIPHY_TRANSLATE_API, params=query)
            data.raise_for_status()
        except ConnectionError as e:
            raise ConfigValidationError(str(e))
        except HTTPError as e:
            error_message = str(e)
            if data.status_code == 403:
                error_message += ('This is likely due to an invalid key.\n'
                                  'Follow the instructions in doc.md for setting an API key.')
            raise ConfigValidationError(error_message)

    def initialize(self, __tmp3: <FILL>) -> None:
        self.config_info = __tmp3.get_config_info('giphy')

    def handle_message(self, __tmp0: Dict[str, str], __tmp3) :
        bot_response = get_bot_giphy_response(
            __tmp0,
            __tmp3,
            self.config_info
        )
        __tmp3.send_reply(__tmp0, bot_response)


class __typ0(Exception):
    pass


def __tmp2(__tmp1: str, api_key: str) -> Union[int, str]:
    # Return a URL for a Giphy GIF based on keywords given.
    # In case of error, e.g. failure to fetch a GIF URL, it will
    # return a number.
    query = {'api_key': api_key}
    if len(__tmp1) > 0:
        query['s'] = __tmp1
        url = GIPHY_TRANSLATE_API
    else:
        url = GIPHY_RANDOM_API

    try:
        data = requests.get(url, params=query)
    except requests.exceptions.ConnectionError as e:  # Usually triggered by bad connection.
        logging.exception('Bad connection')
        raise
    data.raise_for_status()

    try:
        gif_url = data.json()['data']['images']['original']['url']
    except (TypeError, KeyError):  # Usually triggered by no result in Giphy.
        raise __typ0()
    return gif_url


def get_bot_giphy_response(__tmp0: Dict[str, str], __tmp3, config_info) -> str:
    # Each exception has a specific reply should "gif_url" return a number.
    # The bot will post the appropriate message for the error.
    __tmp1 = __tmp0['content']
    try:
        gif_url = __tmp2(__tmp1, config_info['key'])
    except requests.exceptions.ConnectionError:
        return ('Uh oh, sorry :slightly_frowning_face:, I '
                'cannot process your request right now. But, '
                'let\'s try again later! :grin:')
    except __typ0:
        return ('Sorry, I don\'t have a GIF for "%s"! '
                ':astonished:' % (__tmp1))
    return ('[Click to enlarge](%s)'
            '[](/static/images/interactive-bot/giphy/powered-by-giphy.png)'
            % (gif_url))

handler_class = __typ1
