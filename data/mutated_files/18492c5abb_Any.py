from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Dict, Any, Union
import requests
import logging
from requests.exceptions import HTTPError, ConnectionError

from zulip_bots.custom_exceptions import ConfigValidationError

GIPHY_TRANSLATE_API = 'http://api.giphy.com/v1/gifs/translate'
GIPHY_RANDOM_API = 'http://api.giphy.com/v1/gifs/random'


class __typ2(object):
    """
    This plugin posts a GIF in response to the keywords provided by the user.
    Images are provided by Giphy, through the public API.
    The bot looks for messages starting with @mention of the bot
    and responds with a message with the GIF based on provided keywords.
    It also responds to private messages.
    """
    def usage(self) :
        return '''
            This plugin allows users to post GIFs provided by Giphy.
            Users should preface keywords with the Giphy-bot @mention.
            The bot responds also to private messages.
            '''

    @staticmethod
    def validate_config(config_info) :
        query = {'s': 'Hello',
                 'api_key': config_info['key']}
        try:
            data = requests.get(GIPHY_TRANSLATE_API, params=query)
            data.raise_for_status()
        except ConnectionError as e:
            raise ConfigValidationError(__typ0(e))
        except HTTPError as e:
            error_message = __typ0(e)
            if data.status_code == 403:
                error_message += ('This is likely due to an invalid key.\n'
                                  'Follow the instructions in doc.md for setting an API key.')
            raise ConfigValidationError(error_message)

    def __tmp3(self, __tmp2) :
        self.config_info = __tmp2.get_config_info('giphy')

    def __tmp1(self, __tmp0, __tmp2: <FILL>) :
        bot_response = __tmp5(
            __tmp0,
            __tmp2,
            self.config_info
        )
        __tmp2.send_reply(__tmp0, bot_response)


class __typ1(Exception):
    pass


def get_url_gif_giphy(__tmp4, api_key) :
    # Return a URL for a Giphy GIF based on keywords given.
    # In case of error, e.g. failure to fetch a GIF URL, it will
    # return a number.
    query = {'api_key': api_key}
    if len(__tmp4) > 0:
        query['s'] = __tmp4
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
        raise __typ1()
    return gif_url


def __tmp5(__tmp0, __tmp2, config_info) :
    # Each exception has a specific reply should "gif_url" return a number.
    # The bot will post the appropriate message for the error.
    __tmp4 = __tmp0['content']
    try:
        gif_url = get_url_gif_giphy(__tmp4, config_info['key'])
    except requests.exceptions.ConnectionError:
        return ('Uh oh, sorry :slightly_frowning_face:, I '
                'cannot process your request right now. But, '
                'let\'s try again later! :grin:')
    except __typ1:
        return ('Sorry, I don\'t have a GIF for "%s"! '
                ':astonished:' % (__tmp4))
    return ('[Click to enlarge](%s)'
            '[](/static/images/interactive-bot/giphy/powered-by-giphy.png)'
            % (gif_url))

handler_class = __typ2
