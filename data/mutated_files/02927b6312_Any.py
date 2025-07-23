from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
import random

import logging
import requests

from typing import Any, Dict, Optional

XKCD_TEMPLATE_URL = 'https://xkcd.com/%s/info.0.json'
LATEST_XKCD_URL = 'https://xkcd.com/info.0.json'

class __typ2(object):
    '''
    This plugin provides several commands that can be used for fetch a comic
    strip from https://xkcd.com. The bot looks for messages starting with
    "@mention-bot" and responds with a message with the comic based on provided
    commands.
    '''

    META = {
        'name': 'XKCD',
        'description': 'Fetches comic strips from https://xkcd.com.',
    }

    def usage(__tmp2) -> __typ1:
        return '''
            This plugin allows users to fetch a comic strip provided by
            https://xkcd.com. Users should preface the command with "@mention-bot".

            There are several commands to use this bot:
            - @mention-bot help -> To show all commands the bot supports.
            - @mention-bot latest -> To fetch the latest comic strip from xkcd.
            - @mention-bot random -> To fetch a random comic strip from xkcd.
            - @mention-bot <comic_id> -> To fetch a comic strip based on
            `<comic_id>`, e.g `@mention-bot 1234`.
            '''

    def handle_message(__tmp2, __tmp0: Dict[__typ1, __typ1], __tmp3: <FILL>) -> None:
        __tmp6 = __tmp3.identity().mention
        xkcd_bot_response = __tmp1(__tmp0, __tmp6)
        __tmp3.send_reply(__tmp0, xkcd_bot_response)

class __typ5(object):
    LATEST = 0
    RANDOM = 1
    COMIC_ID = 2

class __typ4(Exception):
    pass

class __typ3(Exception):
    pass

def __tmp1(__tmp0: Dict[__typ1, __typ1], __tmp6) -> __typ1:
    original_content = __tmp0['content'].strip()
    command = original_content.strip()

    commands_help = ("%s"
                     "\n* `{0} help` to show this help message."
                     "\n* `{0} latest` to fetch the latest comic strip from xkcd."
                     "\n* `{0} random` to fetch a random comic strip from xkcd."
                     "\n* `{0} <comic id>` to fetch a comic strip based on `<comic id>` "
                     "e.g `{0} 1234`.".format(__tmp6))

    try:
        if command == 'help':
            return commands_help % ('xkcd bot supports these commands:')
        elif command == 'latest':
            fetched = __tmp5(__typ5.LATEST)
        elif command == 'random':
            fetched = __tmp5(__typ5.RANDOM)
        elif command.isdigit():
            fetched = __tmp5(__typ5.COMIC_ID, command)
        else:
            return commands_help % ("xkcd bot only supports these commands, not `%s`:" % (command,))
    except (requests.exceptions.ConnectionError, __typ3):
        logging.exception('Connection error occurred when trying to connect to xkcd server')
        return 'Sorry, I cannot process your request right now, please try again later!'
    except __typ4:
        logging.exception('XKCD server responded 404 when trying to fetch comic with id %s'
                          % (command))
        return 'Sorry, there is likely no xkcd comic strip with id: #%s' % (command,)
    else:
        return ("#%s: **%s**\n[%s](%s)" % (fetched['num'],
                                           fetched['title'],
                                           fetched['alt'],
                                           fetched['img']))

def __tmp5(__tmp4, comic_id: Optional[__typ1]=None) -> Dict[__typ1, __typ1]:
    try:
        if __tmp4 == __typ5.LATEST:  # Fetch the latest comic strip.
            url = LATEST_XKCD_URL

        elif __tmp4 == __typ5.RANDOM:  # Fetch a random comic strip.
            latest = requests.get(LATEST_XKCD_URL)

            if latest.status_code != 200:
                raise __typ3()

            latest_id = latest.json()['num']
            random_id = random.randint(1, latest_id)
            url = XKCD_TEMPLATE_URL % (__typ1(random_id))

        elif __tmp4 == __typ5.COMIC_ID:  # Fetch specific comic strip by id number.
            if comic_id is None:
                raise Exception('Missing comic_id argument')
            url = XKCD_TEMPLATE_URL % (comic_id)

        fetched = requests.get(url)

        if fetched.status_code == 404:
            raise __typ4()
        elif fetched.status_code != 200:
            raise __typ3()

        xkcd_json = fetched.json()
    except requests.exceptions.ConnectionError as e:
        logging.exception("Connection Error")
        raise

    return xkcd_json

handler_class = __typ2
