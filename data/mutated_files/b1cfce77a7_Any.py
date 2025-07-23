import logging
from typing import Dict, Any

from zulip_bots.bots.monkeytestit.lib import parse
from zulip_bots.lib import NoBotConfigException


class __typ0(object):
    def __init__(__tmp1):
        __tmp1.api_key = "None"
        __tmp1.config = None

    def usage(__tmp1):
        return "Remember to set your api_key first in the config. After " \
               "that, to perform a check, mention me and add the website.\n\n" \
               "Check doc.md for more options and setup instructions."

    def initialize(__tmp1, bot_handler) :
        try:
            __tmp1.config = bot_handler.get_config_info('monkeytestit')
        except NoBotConfigException:
            bot_handler.quit("Quitting because there's no config file "
                             "supplied. See doc.md for a guide on setting up "
                             "one. If you already know the drill, just create "
                             "a .conf file with \"monkeytestit\" as the "
                             "section header and api_key = <your key> for "
                             "the api key.")

        __tmp1.api_key = __tmp1.config.get('api_key')

        if not __tmp1.api_key:
            bot_handler.quit("Config file exists, but can't find api_key key "
                             "or value. Perhaps it is misconfigured. Check "
                             "doc.md for details on how to setup the config.")

        logging.info("Checking validity of API key. This will take a while.")

        if "wrong secret" in parse.execute("check https://website",
                                           __tmp1.api_key).lower():
            bot_handler.quit("API key exists, but it is not valid. Reconfigure"
                             " your api_key value and try again.")

    def handle_message(__tmp1, __tmp0,
                       bot_handler: <FILL>) -> None:
        content = __tmp0['content']

        response = parse.execute(content, __tmp1.api_key)

        bot_handler.send_reply(__tmp0, response)


handler_class = __typ0
