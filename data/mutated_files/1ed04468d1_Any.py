from typing import TypeAlias
__typ0 : TypeAlias = "str"
# See readme.md for instructions on running this code.

import requests
from typing import Any, List, Dict
import logging

class MentionHandler(object):
    def initialize(__tmp1, __tmp2: Any) -> None:
        __tmp1.config_info = __tmp2.get_config_info('mention')
        __tmp1.access_token = __tmp1.config_info['access_token']
        __tmp1.account_id = ''

        __tmp1.check_access_token(__tmp2)

    def check_access_token(__tmp1, __tmp2: <FILL>) -> None:
        test_query_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Accept-Version': '1.15',
        }
        test_query_response = requests.get('https://api.mention.net/api/accounts/me', headers=test_query_header)

        try:
            test_query_data = test_query_response.json()
            if test_query_data['error'] == 'invalid_grant' and \
               test_query_data['error_description'] == 'The access token provided is invalid.':
                __tmp2.quit('Access Token Invalid. Please see doc.md to find out how to get it.')
        except KeyError:
            pass

    def usage(__tmp1) :
        return '''
        This is a Mention API Bot which will find mentions
        of the given keyword throughout the web.
        Version 1.00
        '''

    def handle_message(__tmp1, message, __tmp2) :
        message['content'] = message['content'].strip()

        if message['content'].lower() == 'help':
            __tmp2.send_reply(message, __tmp1.usage())
            return

        if message['content'] == '':
            __tmp2.send_reply(message, 'Empty Mention Query')
            return

        __tmp0 = message['content']
        content = __tmp1.generate_response(__tmp0)
        __tmp2.send_reply(message, content)

    def get_account_id(__tmp1) -> __typ0:
        get_ac_id_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Accept-Version': '1.15',
        }
        response = requests.get('https://api.mention.net/api/accounts/me', headers=get_ac_id_header)
        data_json = response.json()
        account_id = data_json['account']['id']
        return account_id

    def get_alert_id(__tmp1, __tmp0: __typ0) -> __typ0:
        create_alert_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Content-Type': 'application/json',
            'Accept-Version': '1.15',
        }

        create_alert_data = {
            'name': __tmp0,
            'query': {
                'type': 'basic',
                'included_keywords': [__tmp0]
            },
            'languages': ['en'],
            'sources': ['web']
        }  # type: Any

        response = requests.post('https://api.mention.net/api/accounts/' + __tmp1.account_id +
                                 '/alerts', data=create_alert_data, headers=create_alert_header)
        data_json = response.json()
        __tmp3 = data_json['alert']['id']
        return __tmp3

    def get_mentions(__tmp1, __tmp3: __typ0) -> List[Any]:
        get_mentions_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Accept-Version': '1.15',
        }
        response = requests.get('https://api.mention.net/api/accounts/' + __tmp1.account_id +
                                '/alerts/' + __tmp3 + '/mentions', headers=get_mentions_header)
        data_json = response.json()
        mentions = data_json['mentions']
        return mentions

    def generate_response(__tmp1, __tmp0) -> __typ0:
        if __tmp1.account_id == '':
            __tmp1.account_id = __tmp1.get_account_id()

        try:
            __tmp3 = __tmp1.get_alert_id(__tmp0)
        except (TypeError, KeyError):
            # Usually triggered by invalid token or json parse error when account quote is finished.
            raise __typ1()

        try:
            mentions = __tmp1.get_mentions(__tmp3)
        except (TypeError, KeyError):
            # Usually triggered by no response or json parse error when account quota is finished.
            raise __typ1()

        reply = 'The most recent mentions of `' + __tmp0 + '` on the web are: \n'
        for mention in mentions:
            reply += "[{title}]({id})\n".format(title=mention['title'], id=mention['original_url'])
        return reply

handler_class = MentionHandler

class __typ1(Exception):
    pass
