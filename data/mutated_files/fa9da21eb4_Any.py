from typing import TypeAlias
__typ0 : TypeAlias = "str"
import requests
import logging
import sys

from requests.exceptions import HTTPError, ConnectionError
from typing import Dict, Any, Union, List, Tuple, Optional

commands_list = ('list', 'top', 'help')

class __typ1(object):

    def __tmp7(self) :
        return '''
            This plugin will allow users to search
            for a given search term on Youtube.
            Use '@mention-bot help' to get more information on the bot usage.
            '''
    help_content = "*Help for YouTube bot* :robot_face: : \n\n" \
                   "The bot responds to messages starting with @mention-bot.\n\n" \
                   "`@mention-bot <search terms>` will return top Youtube video for the given `<search term>`.\n" \
                   "`@mention-bot top <search terms>` also returns the top Youtube result.\n" \
                   "`@mention-bot list <search terms>` will return a list Youtube videos for the given <search term>.\n \n" \
                   "Example:\n" \
                   " * @mention-bot funny cats\n" \
                   " * @mention-bot list funny dogs"

    def __tmp5(self, __tmp3) :
        self.config_info = __tmp3.get_config_info('youtube')
        # Check if API key is valid. If it is not valid, don't run the bot.
        try:
            search_youtube('test', self.config_info['key'], self.config_info['video_region'])
        except HTTPError as e:
            if (e.response.json()['error']['errors'][0]['reason'] == 'keyInvalid'):
                __tmp3.quit('Invalid key.'
                                 'Follow the instructions in doc.md for setting API key.')
            else:
                raise
        except ConnectionError:
            logging.warning('Bad connection')

    def __tmp2(self, __tmp0, __tmp3: <FILL>) :

        if __tmp0['content'] == '' or __tmp0['content'] == 'help':
            __tmp3.send_reply(__tmp0, self.help_content)
        else:
            cmd, __tmp4 = get_command_query(__tmp0)
            bot_response = __tmp1(__tmp4,
                                            cmd,
                                            self.config_info)
            logging.info(bot_response.format())
            __tmp3.send_reply(__tmp0, bot_response)


def search_youtube(__tmp4, __tmp6,
                   region, max_results: int = 1) :

    videos = []
    params = {
        'part': 'id,snippet',
        'maxResults': max_results,
        'key': __tmp6,
        'q': __tmp4,
        'alt': 'json',
        'type': 'video',
        'regionCode': region}  # type: Dict[str, Union[str, int]]

    url = 'https://www.googleapis.com/youtube/v3/search'
    try:
        r = requests.get(url, params=params)
    except ConnectionError as e:  # Usually triggered by bad connection.
        logging.exception('Bad connection')
        raise
    r.raise_for_status()
    search_response = r.json()
    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append([search_result['snippet']['title'],
                           search_result['id']['videoId']])
    return videos


def get_command_query(__tmp0) -> Tuple[Optional[__typ0], __typ0]:
    blocks = __tmp0['content'].lower().split()
    command = blocks[0]
    if command in commands_list:
        __tmp4 = __tmp0['content'][len(command) + 1:].lstrip()
        return command, __tmp4
    else:
        return None, __tmp0['content']


def __tmp1(__tmp4, command, config_info: Dict[__typ0, __typ0]) :

    __tmp6 = config_info['key']
    max_results = int(config_info['number_of_results'])
    region = config_info['video_region']
    video_list = []   # type: List[List[str]]
    try:
        if __tmp4 == '' or __tmp4 is None:
            return __typ1.help_content
        if command is None or command == 'top':
            video_list = search_youtube(__tmp4, __tmp6, region)

        elif command == 'list':
            video_list = search_youtube(__tmp4, __tmp6, region, max_results)

        elif command == 'help':
            return __typ1.help_content

    except (ConnectionError, HTTPError):
        return 'Uh-Oh, couldn\'t process the request ' \
               'right now.\nPlease again later'

    reply = 'Here is what I found for `' + __tmp4 + '` : '

    if len(video_list) == 0:
        return 'Oops ! Sorry I couldn\'t find any video for  `' + __tmp4 + '` :slightly_frowning_face:'
    elif len(video_list) == 1:
        return (reply + '\n%s - [Watch now](https://www.youtube.com/watch?v=%s)' % (video_list[0][0], video_list[0][1])).strip()

    for title, id in video_list:
        reply = reply + \
            '\n * %s - [Watch now](https://www.youtube.com/watch/%s)' % (title, id)
    # Using link https://www.youtube.com/watch/<id> to
    # prevent showing multiple previews
    return reply


handler_class = __typ1
