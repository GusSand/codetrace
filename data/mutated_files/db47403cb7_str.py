from typing import TypeAlias
__typ1 : TypeAlias = "Any"
import requests
import logging
import sys

from requests.exceptions import HTTPError, ConnectionError
from typing import Dict, Any, Union, List, Tuple, Optional

commands_list = ('list', 'top', 'help')

class __typ0(object):

    def __tmp4(__tmp1) -> str:
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

    def initialize(__tmp1, __tmp2: __typ1) -> None:
        __tmp1.config_info = __tmp2.get_config_info('youtube')
        # Check if API key is valid. If it is not valid, don't run the bot.
        try:
            search_youtube('test', __tmp1.config_info['key'], __tmp1.config_info['video_region'])
        except HTTPError as e:
            if (e.response.json()['error']['errors'][0]['reason'] == 'keyInvalid'):
                __tmp2.quit('Invalid key.'
                                 'Follow the instructions in doc.md for setting API key.')
            else:
                raise
        except ConnectionError:
            logging.warning('Bad connection')

    def handle_message(__tmp1, __tmp0: Dict[str, str], __tmp2: __typ1) -> None:

        if __tmp0['content'] == '' or __tmp0['content'] == 'help':
            __tmp2.send_reply(__tmp0, __tmp1.help_content)
        else:
            cmd, __tmp3 = get_command_query(__tmp0)
            bot_response = get_bot_response(__tmp3,
                                            cmd,
                                            __tmp1.config_info)
            logging.info(bot_response.format())
            __tmp2.send_reply(__tmp0, bot_response)


def search_youtube(__tmp3: <FILL>, key: str,
                   __tmp5, max_results: int = 1) -> List[List[str]]:

    videos = []
    params = {
        'part': 'id,snippet',
        'maxResults': max_results,
        'key': key,
        'q': __tmp3,
        'alt': 'json',
        'type': 'video',
        'regionCode': __tmp5}  # type: Dict[str, Union[str, int]]

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


def get_command_query(__tmp0: Dict[str, str]) -> Tuple[Optional[str], str]:
    blocks = __tmp0['content'].lower().split()
    command = blocks[0]
    if command in commands_list:
        __tmp3 = __tmp0['content'][len(command) + 1:].lstrip()
        return command, __tmp3
    else:
        return None, __tmp0['content']


def get_bot_response(__tmp3: Optional[str], command: Optional[str], config_info: Dict[str, str]) :

    key = config_info['key']
    max_results = int(config_info['number_of_results'])
    __tmp5 = config_info['video_region']
    video_list = []   # type: List[List[str]]
    try:
        if __tmp3 == '' or __tmp3 is None:
            return __typ0.help_content
        if command is None or command == 'top':
            video_list = search_youtube(__tmp3, key, __tmp5)

        elif command == 'list':
            video_list = search_youtube(__tmp3, key, __tmp5, max_results)

        elif command == 'help':
            return __typ0.help_content

    except (ConnectionError, HTTPError):
        return 'Uh-Oh, couldn\'t process the request ' \
               'right now.\nPlease again later'

    reply = 'Here is what I found for `' + __tmp3 + '` : '

    if len(video_list) == 0:
        return 'Oops ! Sorry I couldn\'t find any video for  `' + __tmp3 + '` :slightly_frowning_face:'
    elif len(video_list) == 1:
        return (reply + '\n%s - [Watch now](https://www.youtube.com/watch?v=%s)' % (video_list[0][0], video_list[0][1])).strip()

    for title, id in video_list:
        reply = reply + \
            '\n * %s - [Watch now](https://www.youtube.com/watch/%s)' % (title, id)
    # Using link https://www.youtube.com/watch/<id> to
    # prevent showing multiple previews
    return reply


handler_class = __typ0
