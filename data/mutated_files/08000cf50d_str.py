# See readme.md for instructions on running this code.

import requests
from typing import Any, List, Dict
import logging

class __typ1(object):
    def __tmp5(__tmp1, __tmp3) :
        __tmp1.config_info = __tmp3.get_config_info('mention')
        __tmp1.access_token = __tmp1.config_info['access_token']
        __tmp1.account_id = ''

        __tmp1.check_access_token(__tmp3)

    def check_access_token(__tmp1, __tmp3) -> None:
        test_query_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Accept-Version': '1.15',
        }
        test_query_response = requests.get('https://api.mention.net/api/accounts/me', headers=test_query_header)

        try:
            test_query_data = test_query_response.json()
            if test_query_data['error'] == 'invalid_grant' and \
               test_query_data['error_description'] == 'The access token provided is invalid.':
                __tmp3.quit('Access Token Invalid. Please see doc.md to find out how to get it.')
        except KeyError:
            pass

    def usage(__tmp1) :
        return '''
        This is a Mention API Bot which will find mentions
        of the given keyword throughout the web.
        Version 1.00
        '''

    def __tmp2(__tmp1, __tmp0, __tmp3) :
        __tmp0['content'] = __tmp0['content'].strip()

        if __tmp0['content'].lower() == 'help':
            __tmp3.send_reply(__tmp0, __tmp1.usage())
            return

        if __tmp0['content'] == '':
            __tmp3.send_reply(__tmp0, 'Empty Mention Query')
            return

        __tmp6 = __tmp0['content']
        content = __tmp1.generate_response(__tmp6)
        __tmp3.send_reply(__tmp0, content)

    def get_account_id(__tmp1) -> str:
        get_ac_id_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Accept-Version': '1.15',
        }
        response = requests.get('https://api.mention.net/api/accounts/me', headers=get_ac_id_header)
        data_json = response.json()
        account_id = data_json['account']['id']
        return account_id

    def get_alert_id(__tmp1, __tmp6: <FILL>) -> str:
        create_alert_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Content-Type': 'application/json',
            'Accept-Version': '1.15',
        }

        create_alert_data = {
            'name': __tmp6,
            'query': {
                'type': 'basic',
                'included_keywords': [__tmp6]
            },
            'languages': ['en'],
            'sources': ['web']
        }  # type: Any

        response = requests.post('https://api.mention.net/api/accounts/' + __tmp1.account_id +
                                 '/alerts', data=create_alert_data, headers=create_alert_header)
        data_json = response.json()
        __tmp4 = data_json['alert']['id']
        return __tmp4

    def get_mentions(__tmp1, __tmp4: str) -> List[Any]:
        get_mentions_header = {
            'Authorization': 'Bearer ' + __tmp1.access_token,
            'Accept-Version': '1.15',
        }
        response = requests.get('https://api.mention.net/api/accounts/' + __tmp1.account_id +
                                '/alerts/' + __tmp4 + '/mentions', headers=get_mentions_header)
        data_json = response.json()
        mentions = data_json['mentions']
        return mentions

    def generate_response(__tmp1, __tmp6: str) -> str:
        if __tmp1.account_id == '':
            __tmp1.account_id = __tmp1.get_account_id()

        try:
            __tmp4 = __tmp1.get_alert_id(__tmp6)
        except (TypeError, KeyError):
            # Usually triggered by invalid token or json parse error when account quote is finished.
            raise __typ0()

        try:
            mentions = __tmp1.get_mentions(__tmp4)
        except (TypeError, KeyError):
            # Usually triggered by no response or json parse error when account quota is finished.
            raise __typ0()

        reply = 'The most recent mentions of `' + __tmp6 + '` on the web are: \n'
        for mention in mentions:
            reply += "[{title}]({id})\n".format(title=mention['title'], id=mention['original_url'])
        return reply

handler_class = __typ1

class __typ0(Exception):
    pass
