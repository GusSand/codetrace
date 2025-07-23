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
def __tmp11(__tmp8, __tmp4) :
    for user in __tmp8:
        if __tmp4 == user['firstName']:
            return user['id']

# Make request to given flock URL and return a two-element tuple
# whose left-hand value contains JSON body of response (or None if request failed)
# and whose right-hand value contains an error message (or None if request succeeded)
def __tmp15(__tmp6: <FILL>, __tmp12) :
    try:
        res = requests.get(__tmp6, __tmp12=__tmp12)
        return (res.json(), None)
    except ConnectionError as e:
        logging.exception(str(e))
        error = "Uh-Oh, couldn't process the request \
right now.\nPlease try again later"
        return (None, error)

# Returns two-element tuple whose left-hand value contains recipient
# user's ID (or None if it was not found) and right-hand value contains
# an error message (or None if recipient user's ID was found)
def get_recipient_id(__tmp4, __tmp9) :
    token = __tmp9['token']
    payload = {
        'token': token
    }
    __tmp8, error = __tmp15(USERS_LIST_URL, payload)
    if __tmp8 is None:
        return (None, error)

    recipient_id = __tmp11(__tmp8, __tmp4)
    if recipient_id is None:
        error = "No user found. Make sure you typed it correctly."
        return (None, error)
    else:
        return (recipient_id, None)

# This handles the message sending work.
def __tmp10(__tmp7, __tmp9) -> str:
    token = __tmp9['token']
    content_pieces = __tmp7.split(':')
    __tmp4 = content_pieces[0].strip()
    __tmp0 = content_pieces[1].strip()

    recipient_id, error = get_recipient_id(__tmp4, __tmp9)
    if recipient_id is None:
        return error

    if len(str(recipient_id)) > 30:
        return "Found user is invalid."

    payload = {
        'to': recipient_id,
        'text': __tmp0,
        'token': token
    }
    res, error = __tmp15(SEND_MESSAGE_URL, payload)
    if res is None:
        return error

    if "uid" in res:
        return "Message sent."
    else:
        return "Message sending failed :slightly_frowning_face:. Please try again."

def __tmp14(__tmp7, __tmp9: Dict[str, str]) :
    __tmp7 = __tmp7.strip()
    if __tmp7 == '' or __tmp7 == 'help':
        return help_message
    else:
        result = __tmp10(__tmp7, __tmp9)
        return result

class FlockHandler(object):
    '''
    This is flock bot. Now you can send messages to any of your
    flock user without having to leave Zulip.
    '''

    def __tmp5(__tmp1, __tmp3) :
        __tmp1.config_info = __tmp3.get_config_info('flock')

    def __tmp13(__tmp1) :
        return '''Hello from Flock Bot. You can send messages to any Flock user
right from Zulip.'''

    def __tmp2(__tmp1, __tmp0, __tmp3) -> None:
        response = __tmp14(__tmp0['content'], __tmp1.config_info)
        __tmp3.send_reply(__tmp0, response)

handler_class = FlockHandler
