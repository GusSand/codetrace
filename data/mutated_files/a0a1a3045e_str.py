import logging
import requests
from typing import Any, Dict, List, Tuple, Optional
from requests.exceptions import ConnectionError

USERS_LIST_URL = 'https://api.flock.co/v1/roster.listContacts'
SEND_MESSAGE_URL = 'https://api.flock.co/v1/chat.sendMessage'

help_message = '''
You can send messages to any Flock user associated with your account from Zulip.
*Syntax*: **@botname to: message** where `to` is **firstName** of recipient.
'''

# Matches the recipient name provided by user with list of users in his contacts.
# If matches, returns the matched User's ID
def __tmp6(__tmp4: List[Any], recipient_name) -> str:
    for user in __tmp4:
        if recipient_name == user['firstName']:
            return user['id']

# Make request to given flock URL and return a two-element tuple
# whose left-hand value contains JSON body of response (or None if request failed)
# and whose right-hand value contains an error message (or None if request succeeded)
def __tmp10(url: str, params: Dict[str, str]) :
    try:
        res = requests.get(url, params=params)
        return (res.json(), None)
    except ConnectionError as e:
        logging.exception(str(e))
        error = "Uh-Oh, couldn't process the request \
right now.\nPlease try again later"
        return (None, error)

# Returns two-element tuple whose left-hand value contains recipient
# user's ID (or None if it was not found) and right-hand value contains
# an error message (or None if recipient user's ID was found)
def get_recipient_id(recipient_name: str, __tmp5) -> Tuple[Optional[str], Optional[str]]:
    token = __tmp5['token']
    payload = {
        'token': token
    }
    __tmp4, error = __tmp10(USERS_LIST_URL, payload)
    if __tmp4 is None:
        return (None, error)

    recipient_id = __tmp6(__tmp4, recipient_name)
    if recipient_id is None:
        error = "No user found. Make sure you typed it correctly."
        return (None, error)
    else:
        return (recipient_id, None)

# This handles the message sending work.
def __tmp7(content: <FILL>, __tmp5) -> str:
    token = __tmp5['token']
    content_pieces = content.split(':')
    recipient_name = content_pieces[0].strip()
    __tmp0 = content_pieces[1].strip()

    recipient_id, error = get_recipient_id(recipient_name, __tmp5)
    if recipient_id is None:
        return error

    if len(str(recipient_id)) > 30:
        return "Found user is invalid."

    payload = {
        'to': recipient_id,
        'text': __tmp0,
        'token': token
    }
    res, error = __tmp10(SEND_MESSAGE_URL, payload)
    if res is None:
        return error

    if "uid" in res:
        return "Message sent."
    else:
        return "Message sending failed :slightly_frowning_face:. Please try again."

def __tmp9(content, __tmp5: Dict[str, str]) -> None:
    content = content.strip()
    if content == '' or content == 'help':
        return help_message
    else:
        result = __tmp7(content, __tmp5)
        return result

class FlockHandler(object):
    '''
    This is flock bot. Now you can send messages to any of your
    flock user without having to leave Zulip.
    '''

    def __tmp3(__tmp1, bot_handler: Any) :
        __tmp1.config_info = bot_handler.get_config_info('flock')

    def __tmp8(__tmp1) -> str:
        return '''Hello from Flock Bot. You can send messages to any Flock user
right from Zulip.'''

    def __tmp2(__tmp1, __tmp0, bot_handler) -> None:
        response = __tmp9(__tmp0['content'], __tmp1.config_info)
        bot_handler.send_reply(__tmp0, response)

handler_class = FlockHandler
