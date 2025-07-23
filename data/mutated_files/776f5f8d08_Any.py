import requests
import logging
import json
from typing import Dict, Any, List
from requests.exceptions import HTTPError, ConnectionError

help_message = '''
You can add datapoints towards your beeminder goals \
following the syntax shown below :smile:.\n \
\n**@mention-botname daystamp, value, comment**\
\n* `daystamp`**:** *yyyymmdd*  \
[**NOTE:** Optional field, default is *current daystamp*],\
\n* `value`**:** Enter a value [**NOTE:** Required field, can be any number],\
\n* `comment`**:** Add a comment [**NOTE:** Optional field, default is *None*]\
'''

def get_beeminder_response(__tmp3, config_info) :
    username = config_info['username']
    goalname = config_info['goalname']
    auth_token = config_info['auth_token']

    __tmp3 = __tmp3.strip()
    if __tmp3 == '' or __tmp3 == 'help':
        return help_message

    url = "https://www.beeminder.com/api/v1/users/{}/goals/{}/datapoints.json".format(username, goalname)
    message_pieces = __tmp3.split(',')
    for i in range(len(message_pieces)):
        message_pieces[i] = message_pieces[i].strip()

    if (len(message_pieces) == 1):
        payload = {
            "value": message_pieces[0],
            "auth_token": auth_token
        }
    elif (len(message_pieces) == 2):
        if (message_pieces[1].isdigit()):
            payload = {
                "daystamp": message_pieces[0],
                "value": message_pieces[1],
                "auth_token": auth_token
            }
        else:
            payload = {
                "value": message_pieces[0],
                "comment": message_pieces[1],
                "auth_token": auth_token
            }
    elif (len(message_pieces) == 3):
        payload = {
            "daystamp": message_pieces[0],
            "value": message_pieces[1],
            "comment": message_pieces[2],
            "auth_token": auth_token
        }
    elif (len(message_pieces) > 3):
        return "Make sure you follow the syntax.\n You can take a look \
at syntax by: @mention-botname help"

    try:
        r = requests.post(url, json=payload)

        if r.status_code != 200:
            if r.status_code == 401:   # Handles case of invalid key and missing key
                return "Error. Check your key!"
            else:
                return "Error occured : {}".format(r.status_code)   # Occures in case of unprocessable entity
        else:
            datapoint_link = "https://www.beeminder.com/{}/{}".format(username, goalname)
            return "[Datapoint]({}) created.".format(datapoint_link)   # Handles the case of successful datapoint creation
    except ConnectionError as e:
        logging.exception(str(e))
        return "Uh-Oh, couldn't process the request \
right now.\nPlease try again later"


class __typ0(object):
    '''
    This plugin allows users to easily add datapoints
    towards their beeminder goals via zulip
    '''

    def initialize(__tmp1, __tmp2) :
        __tmp1.config_info = __tmp2.get_config_info('beeminder')
        # Check for valid auth_token
        auth_token = __tmp1.config_info['auth_token']
        try:
            r = requests.get("https://www.beeminder.com/api/v1/users/me.json", params={'auth_token': auth_token})
            if r.status_code == 401:
                __tmp2.quit('Invalid key!')
        except ConnectionError as e:
            logging.exception(str(e))

    def __tmp0(__tmp1) -> str:
        return "This plugin allows users to add datapoints towards their Beeminder goals"

    def handle_message(__tmp1, message, __tmp2: <FILL>) :
        response = get_beeminder_response(message['content'], __tmp1.config_info)
        __tmp2.send_reply(message, response)

handler_class = __typ0
