from typing import TypeAlias
__typ1 : TypeAlias = "Any"
# See readme.md for instructions on running this code.

import requests
from typing import Any, List, Dict
import logging

class __typ0(object):
    def initialize(__tmp0, bot_handler) :
        __tmp0.config_info = bot_handler.get_config_info('mention')
        __tmp0.access_token = __tmp0.config_info['access_token']
        __tmp0.account_id = ''

        __tmp0.check_access_token(bot_handler)

    def check_access_token(__tmp0, bot_handler) :
        test_query_header = {
            'Authorization': 'Bearer ' + __tmp0.access_token,
            'Accept-Version': '1.15',
        }
        test_query_response = requests.get('https://api.mention.net/api/accounts/me', headers=test_query_header)

        try:
            test_query_data = test_query_response.json()
            if test_query_data['error'] == 'invalid_grant' and \
               test_query_data['error_description'] == 'The access token provided is invalid.':
                bot_handler.quit('Access Token Invalid. Please see doc.md to find out how to get it.')
        except KeyError:
            pass

    def usage(__tmp0) :
        return '''
        This is a Mention API Bot which will find mentions
        of the given keyword throughout the web.
        Version 1.00
        '''

    def handle_message(__tmp0, message, bot_handler) :
        message['content'] = message['content'].strip()

        if message['content'].lower() == 'help':
            bot_handler.send_reply(message, __tmp0.usage())
            return

        if message['content'] == '':
            bot_handler.send_reply(message, 'Empty Mention Query')
            return

        keyword = message['content']
        content = __tmp0.generate_response(keyword)
        bot_handler.send_reply(message, content)

    def get_account_id(__tmp0) :
        get_ac_id_header = {
            'Authorization': 'Bearer ' + __tmp0.access_token,
            'Accept-Version': '1.15',
        }
        response = requests.get('https://api.mention.net/api/accounts/me', headers=get_ac_id_header)
        data_json = response.json()
        account_id = data_json['account']['id']
        return account_id

    def get_alert_id(__tmp0, keyword) :
        create_alert_header = {
            'Authorization': 'Bearer ' + __tmp0.access_token,
            'Content-Type': 'application/json',
            'Accept-Version': '1.15',
        }

        create_alert_data = {
            'name': keyword,
            'query': {
                'type': 'basic',
                'included_keywords': [keyword]
            },
            'languages': ['en'],
            'sources': ['web']
        }  # type: Any

        response = requests.post('https://api.mention.net/api/accounts/' + __tmp0.account_id +
                                 '/alerts', data=create_alert_data, headers=create_alert_header)
        data_json = response.json()
        alert_id = data_json['alert']['id']
        return alert_id

    def get_mentions(__tmp0, alert_id) :
        get_mentions_header = {
            'Authorization': 'Bearer ' + __tmp0.access_token,
            'Accept-Version': '1.15',
        }
        response = requests.get('https://api.mention.net/api/accounts/' + __tmp0.account_id +
                                '/alerts/' + alert_id + '/mentions', headers=get_mentions_header)
        data_json = response.json()
        mentions = data_json['mentions']
        return mentions

    def generate_response(__tmp0, keyword: <FILL>) :
        if __tmp0.account_id == '':
            __tmp0.account_id = __tmp0.get_account_id()

        try:
            alert_id = __tmp0.get_alert_id(keyword)
        except (TypeError, KeyError):
            # Usually triggered by invalid token or json parse error when account quote is finished.
            raise MentionNoResponseException()

        try:
            mentions = __tmp0.get_mentions(alert_id)
        except (TypeError, KeyError):
            # Usually triggered by no response or json parse error when account quota is finished.
            raise MentionNoResponseException()

        reply = 'The most recent mentions of `' + keyword + '` on the web are: \n'
        for mention in mentions:
            reply += "[{title}]({id})\n".format(title=mention['title'], id=mention['original_url'])
        return reply

handler_class = __typ0

class MentionNoResponseException(Exception):
    pass
