import logging
from typing import Dict, Any

from zulip_bots.bots.monkeytestit.lib import parse
from zulip_bots.lib import NoBotConfigException


class MonkeyTestitBot(object):
    def __tmp3(__tmp0):
        __tmp0.api_key = "None"
        __tmp0.config = None

    def __tmp4(__tmp0):
        return "Remember to set your api_key first in the config. After " \
               "that, to perform a check, mention me and add the website.\n\n" \
               "Check doc.md for more options and setup instructions."

    def __tmp2(__tmp0, __tmp1: <FILL>) :
        try:
            __tmp0.config = __tmp1.get_config_info('monkeytestit')
        except NoBotConfigException:
            __tmp1.quit("Quitting because there's no config file "
                             "supplied. See doc.md for a guide on setting up "
                             "one. If you already know the drill, just create "
                             "a .conf file with \"monkeytestit\" as the "
                             "section header and api_key = <your key> for "
                             "the api key.")

        __tmp0.api_key = __tmp0.config.get('api_key')

        if not __tmp0.api_key:
            __tmp1.quit("Config file exists, but can't find api_key key "
                             "or value. Perhaps it is misconfigured. Check "
                             "doc.md for details on how to setup the config.")

        logging.info("Checking validity of API key. This will take a while.")

        if "wrong secret" in parse.execute("check https://website",
                                           __tmp0.api_key).lower():
            __tmp1.quit("API key exists, but it is not valid. Reconfigure"
                             " your api_key value and try again.")

    def handle_message(__tmp0, message,
                       __tmp1) -> None:
        content = message['content']

        response = parse.execute(content, __tmp0.api_key)

        __tmp1.send_reply(message, response)


handler_class = MonkeyTestitBot
