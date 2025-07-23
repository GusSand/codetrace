from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

def __tmp6(__tmp5: __typ0, config: Dict[__typ0, __typ0], sender_id: __typ0) -> __typ0:
    if __tmp5.strip() == '' or __tmp5.strip() == 'help':
        return config['bot_info']
    ai = apiai.ApiAI(config['key'])
    try:
        request = ai.text_request()
        request.session_id = sender_id
        request.query = __tmp5
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
        logging.exception(__typ0(e))
        return 'Error. {}.'.format(__typ0(e))

class DialogFlowHandler(object):
    '''
    This plugin allows users to easily add their own
    DialogFlow bots to zulip
    '''

    def __tmp3(__tmp0, __tmp2: <FILL>) -> None:
        __tmp0.config_info = __tmp2.get_config_info('dialogflow')

    def __tmp4(__tmp0) -> __typ0:
        return '''
            This plugin will allow users to easily add their own
            DialogFlow bots to zulip
            '''

    def __tmp1(__tmp0, message, __tmp2: Any) -> None:
        result = __tmp6(message['content'], __tmp0.config_info, message['sender_id'])
        __tmp2.send_reply(message, result)

handler_class = DialogFlowHandler
