from typing import TypeAlias
__typ3 : TypeAlias = "Any"
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


class __typ1(Exception):
    '''raise this when there is an error with the Mashape Api Key'''

class __typ0(Exception):
    '''raise this when the service is unavailable.'''


class __typ2(object):
    '''
    This bot will allow users to translate a sentence into 'Yoda speak'.
    It looks for messages starting with '@mention-bot'.
    '''
    def __tmp5(__tmp1, __tmp3) -> None:
        __tmp1.api_key = __tmp3.get_config_info('yoda')['api_key']

    def __tmp9(__tmp1) :
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

    def __tmp2(__tmp1, __tmp0, __tmp3) :
        __tmp1.handle_input(__tmp0, __tmp3)

    def send_to_yoda_api(__tmp1, __tmp6) -> str:
        # function for sending sentence to api
        response = requests.get("https://yoda.p.mashape.com/yoda",
                                params=dict(__tmp6=__tmp6),
                                headers={
                                    "X-Mashape-Key": __tmp1.api_key,
                                    "Accept": "text/plain"
                                }
                                )

        if response.status_code == 200:
            return response.json()['text']
        if response.status_code == 403:
            raise __typ1
        if response.status_code == 503:
            raise __typ0
        else:
            error_message = response.json()['message']
            logging.error(error_message)
            error_code = response.status_code
            error_message = error_message + 'Error code: ' + str(error_code) +\
                ' Did you follow the instructions in the `readme.md` file?'
            return error_message

    def format_input(__tmp1, __tmp7: <FILL>) :
        # gets rid of whitespace around the edges, so that they aren't a problem in the future
        message_content = __tmp7.strip()
        # replaces all spaces with '+' to be in the format the api requires
        __tmp6 = message_content.replace(' ', '+')
        return __tmp6

    def handle_input(__tmp1, __tmp0, __tmp3: __typ3) :
        __tmp7 = __tmp0['content']

        if __tmp1.is_help(__tmp7) or (__tmp7 == ""):
            __tmp3.send_reply(__tmp0, HELP_MESSAGE)

        else:
            __tmp6 = __tmp1.format_input(__tmp7)
            try:
                reply_message = __tmp1.send_to_yoda_api(__tmp6)

                if len(reply_message) == 0:
                    reply_message = 'Invalid input, please check the sentence you have entered.'

            except ssl.SSLError or TypeError:
                reply_message = 'The service is temporarily unavailable, please try again.'
                logging.error(reply_message)

            except __typ1:
                reply_message = 'Invalid Api Key. Did you follow the instructions in the ' \
                                '`readme.md` file?'
                logging.error(reply_message)

            __tmp3.send_reply(__tmp0, reply_message)

    def send_message(__tmp1, __tmp3, __tmp0, __tmp8: str, __tmp4) :
        # function for sending a message
        __tmp3.send_message(dict(
            type='stream',
            to=__tmp8,
            __tmp4=__tmp4,
            content=__tmp0
        ))

    def is_help(__tmp1, __tmp7) :
        # gets rid of whitespace around the edges, so that they aren't a problem in the future
        message_content = __tmp7.strip()
        if message_content == 'help':
            return True
        else:
            return False

handler_class = __typ2
