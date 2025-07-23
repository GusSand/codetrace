from typing import TypeAlias
__typ1 : TypeAlias = "Any"
# See readme.md for instructions on running this code.
import logging
import ssl
import sys
import requests

from typing import Any, Dict

HELP_MESSAGE = '''
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


class ApiKeyError(Exception):
    '''raise this when there is an error with the Mashape Api Key'''

class __typ0(Exception):
    '''raise this when the service is unavailable.'''


class YodaSpeakHandler(object):
    '''
    This bot will allow users to translate a sentence into 'Yoda speak'.
    It looks for messages starting with '@mention-bot'.
    '''
    def initialize(__tmp0, bot_handler: __typ1) -> None:
        __tmp0.api_key = bot_handler.get_config_info('yoda')['api_key']

    def usage(__tmp0) -> str:
        return '''
            This bot will allow users to translate a sentence into
            'Yoda speak'.
            Users should preface messages with '@mention-bot'.

            Before running this, make sure to get a Mashape Api token.
            Instructions are in the 'readme.md' file.
            Store it in the 'yoda.conf' file.
            The 'yoda.conf' file should be located in this bot's directory.
            Example input:
            @mention-bot You will learn how to speak like me someday.
            '''

    def handle_message(__tmp0, message: Dict[str, str], bot_handler) -> None:
        __tmp0.handle_input(message, bot_handler)

    def send_to_yoda_api(__tmp0, sentence: str) -> str:
        # function for sending sentence to api
        response = requests.get("https://yoda.p.mashape.com/yoda",
                                params=dict(sentence=sentence),
                                headers={
                                    "X-Mashape-Key": __tmp0.api_key,
                                    "Accept": "text/plain"
                                }
                                )

        if response.status_code == 200:
            return response.json()['text']
        if response.status_code == 403:
            raise ApiKeyError
        if response.status_code == 503:
            raise __typ0
        else:
            error_message = response.json()['message']
            logging.error(error_message)
            error_code = response.status_code
            error_message = error_message + 'Error code: ' + str(error_code) +\
                ' Did you follow the instructions in the `readme.md` file?'
            return error_message

    def format_input(__tmp0, original_content) -> str:
        # gets rid of whitespace around the edges, so that they aren't a problem in the future
        message_content = original_content.strip()
        # replaces all spaces with '+' to be in the format the api requires
        sentence = message_content.replace(' ', '+')
        return sentence

    def handle_input(__tmp0, message: Dict[str, str], bot_handler: __typ1) :
        original_content = message['content']

        if __tmp0.is_help(original_content) or (original_content == ""):
            bot_handler.send_reply(message, HELP_MESSAGE)

        else:
            sentence = __tmp0.format_input(original_content)
            try:
                reply_message = __tmp0.send_to_yoda_api(sentence)

                if len(reply_message) == 0:
                    reply_message = 'Invalid input, please check the sentence you have entered.'

            except ssl.SSLError or TypeError:
                reply_message = 'The service is temporarily unavailable, please try again.'
                logging.error(reply_message)

            except ApiKeyError:
                reply_message = 'Invalid Api Key. Did you follow the instructions in the ' \
                                '`readme.md` file?'
                logging.error(reply_message)

            bot_handler.send_reply(message, reply_message)

    def send_message(__tmp0, bot_handler, message: str, stream: <FILL>, subject) -> None:
        # function for sending a message
        bot_handler.send_message(dict(
            type='stream',
            to=stream,
            subject=subject,
            content=message
        ))

    def is_help(__tmp0, original_content: str) :
        # gets rid of whitespace around the edges, so that they aren't a problem in the future
        message_content = original_content.strip()
        if message_content == 'help':
            return True
        else:
            return False

handler_class = YodaSpeakHandler
