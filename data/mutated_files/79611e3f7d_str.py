from typing import TypeAlias
__typ0 : TypeAlias = "Any"
# See readme.md for instructions on running this code.
import logging
from urllib import parse
import json

import apiai

from typing import Dict, Any, List

help_message = '''DialogFlow bot
This bot will interact with dialogflow bots.
Simply send this bot a message, and it will respond depending on the configured bot's behaviour.
'''

def get_bot_result(message_content: <FILL>, __tmp3, __tmp1) :
    if message_content.strip() == '' or message_content.strip() == 'help':
        return __tmp3['bot_info']
    ai = apiai.ApiAI(__tmp3['key'])
    try:
        request = ai.text_request()
        request.session_id = __tmp1
        request.query = message_content
        response = request.getresponse()
        res_str = response.read().decode('utf8', 'ignore')
        res_json = json.loads(res_str)
        if res_json['status']['errorType'] != 'success' and 'result' not in res_json.keys():
            return 'Error {}: {}.'.format(res_json['status']['code'], res_json['status']['errorDetails'])
        if res_json['result']['fulfillment']['speech'] == '':
            if 'alternateResult' in res_json.keys():
                if res_json['alternateResult']['fulfillment']['speech'] != '':
                    return res_json['alternateResult']['fulfillment']['speech']
            return 'Error. No result.'
        return res_json['result']['fulfillment']['speech']
    except Exception as e:
        logging.exception(str(e))
        return 'Error. {}.'.format(str(e))

class __typ1(object):
    '''
    This plugin allows users to easily add their own
    DialogFlow bots to zulip
    '''

    def initialize(__tmp0, __tmp2) :
        __tmp0.config_info = __tmp2.get_config_info('dialogflow')

    def __tmp4(__tmp0) :
        return '''
            This plugin will allow users to easily add their own
            DialogFlow bots to zulip
            '''

    def handle_message(__tmp0, message: Dict[str, str], __tmp2: __typ0) :
        result = get_bot_result(message['content'], __tmp0.config_info, message['sender_id'])
        __tmp2.send_reply(message, result)

handler_class = __typ1
