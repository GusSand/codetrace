import zulip
import tweepy
from typing import Dict, Any, Union, List, Tuple, Optional


class TwitpostBot(object):

    def __tmp5(__tmp2) -> str:
        return ''' This bot posts on twitter from zulip chat itself.
                   Use '@twitpost help' to get more information
                   on the bot usage. '''
    help_content = "*Help for Twitter-post bot* :twitter: : \n\n"\
                   "The bot tweets on twitter when message starts "\
                   "with @twitpost.\n\n"\
                   "`@twitpost tweet <content>` will tweet on twitter " \
                   "with given `<content>`.\n" \
                   "Example:\n" \
                   " * @twitpost tweet hey batman\n"

    def initialize(__tmp2, __tmp3: Any) -> None:
        __tmp2.config_info = __tmp3.get_config_info('twitter')
        auth = tweepy.OAuthHandler(__tmp2.config_info['consumer_key'],
                                   __tmp2.config_info['consumer_secret'])
        auth.set_access_token(__tmp2.config_info['access_token'],
                              __tmp2.config_info['access_token_secret'])
        __tmp2.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    def __tmp4(__tmp2, __tmp0, __tmp3: <FILL>) :
        content = __tmp0["content"]

        if content.strip() == '':
            __tmp3.send_reply(__tmp0, 'Please check help for usage.')
            return

        if content.strip() == 'help':
            __tmp3.send_reply(__tmp0, __tmp2.help_content)
            return

        content = content.split()

        if len(content) > 1 and content[0] == "tweet":
            status = __tmp2.post(" ".join(content[1:]))
            screen_name = status["user"]["screen_name"]
            id_str = status["id_str"]
            bot_reply = "https://twitter.com/{}/status/{}".format(screen_name,
                                                                  id_str)
            bot_reply = "Tweet Posted\n" + bot_reply
            __tmp3.send_reply(__tmp0, bot_reply)

    def post(__tmp2, __tmp1):
        return __tmp2.api.update_status(__tmp1)


handler_class = TwitpostBot
