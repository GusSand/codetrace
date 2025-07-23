from typing import TypeAlias
__typ0 : TypeAlias = "str"
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
def __tmp9(__tmp5: List[Any], recipient_name) :
    for user in __tmp5:
        if recipient_name == user['firstName']:
            return user['id']

# Make request to given flock URL and return a two-element tuple
# whose left-hand value contains JSON body of response (or None if request failed)
# and whose right-hand value contains an error message (or None if request succeeded)
def __tmp7(__tmp4, __tmp10) :
    try:
        res = requests.get(__tmp4, __tmp10=__tmp10)
        return (res.json(), None)
    except ConnectionError as e:
        logging.exception(__typ0(e))
        error = "Uh-Oh, couldn't process the request \
right now.\nPlease try again later"
        return (None, error)

# Returns two-element tuple whose left-hand value contains recipient
# user's ID (or None if it was not found) and right-hand value contains
# an error message (or None if recipient user's ID was found)
def __tmp13(recipient_name, __tmp8) :
    token = __tmp8['token']
    payload = {
        'token': token
    }
    __tmp5, error = __tmp7(USERS_LIST_URL, payload)
    if __tmp5 is None:
        return (None, error)

    recipient_id = __tmp9(__tmp5, recipient_name)
    if recipient_id is None:
        error = "No user found. Make sure you typed it correctly."
        return (None, error)
    else:
        return (recipient_id, None)

# This handles the message sending work.
def get_flock_response(__tmp6, __tmp8) :
    token = __tmp8['token']
    content_pieces = __tmp6.split(':')
    recipient_name = content_pieces[0].strip()
    __tmp0 = content_pieces[1].strip()

    recipient_id, error = __tmp13(recipient_name, __tmp8)
    if recipient_id is None:
        return error

    if len(__typ0(recipient_id)) > 30:
        return "Found user is invalid."

    payload = {
        'to': recipient_id,
        'text': __tmp0,
        'token': token
    }
    res, error = __tmp7(SEND_MESSAGE_URL, payload)
    if res is None:
        return error

    if "uid" in res:
        return "Message sent."
    else:
        return "Message sending failed :slightly_frowning_face:. Please try again."

def __tmp12(__tmp6, __tmp8) :
    __tmp6 = __tmp6.strip()
    if __tmp6 == '' or __tmp6 == 'help':
        return help_message
    else:
        result = get_flock_response(__tmp6, __tmp8)
        return result

class __typ1(object):
    '''
    This is flock bot. Now you can send messages to any of your
    flock user without having to leave Zulip.
    '''

    def initialize(__tmp1, __tmp3) :
        __tmp1.config_info = __tmp3.get_config_info('flock')

    def __tmp11(__tmp1) :
        return '''Hello from Flock Bot. You can send messages to any Flock user
right from Zulip.'''

    def __tmp2(__tmp1, __tmp0, __tmp3: <FILL>) :
        response = __tmp12(__tmp0['content'], __tmp1.config_info)
        __tmp3.send_reply(__tmp0, response)

handler_class = __typ1
