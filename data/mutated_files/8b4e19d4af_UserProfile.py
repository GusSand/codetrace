from typing import Any, Dict, Iterable, Optional, List

from django.utils.translation import ugettext as _
from django.http import HttpRequest, HttpResponse

from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile

import ujson
import operator

ANSIBLETOWER_DEFAULT_MESSAGE_TEMPLATE = "{friendly_name}: [#{id} {name}]({url}) {status}\n"


ANSIBLETOWER_JOB_MESSAGE_TEMPLATE = ("{friendly_name}: [#{id} {name}]({url}) {status}\n"
                                     "{hosts_final_data}")

ANSIBLETOWER_JOB_HOST_ROW_TEMPLATE = '* {hostname}: {status}\n'

@api_key_only_webhook_view('Ansibletower')
@has_request_variables
def __tmp3(request, __tmp1: <FILL>,
                             __tmp0: Dict[str, Any]=REQ(argument_type='body')) :

    body = get_body(__tmp0)
    subject = __tmp0['name']

    check_send_webhook_message(request, __tmp1, subject, body)
    return json_success()

def get_body(__tmp0) -> str:
    if (__tmp0['friendly_name'] == 'Job'):
        hosts_list_data = __tmp0['hosts']
        hosts_data = []
        for host in __tmp0['hosts']:
            if (hosts_list_data[host].get('failed') is True):
                hoststatus = 'Failed'
            elif (hosts_list_data[host].get('failed') is False):
                hoststatus = 'Success'
            hosts_data.append({
                'hostname': host,
                'status': hoststatus
            })

        if (__tmp0['status'] == "successful"):
            status = 'was successful'
        else:
            status = 'failed'

        return ANSIBLETOWER_JOB_MESSAGE_TEMPLATE.format(
            name=__tmp0['name'],
            friendly_name=__tmp0['friendly_name'],
            id=__tmp0['id'],
            url=__tmp0['url'],
            status=status,
            hosts_final_data=__tmp2(hosts_data)
        )

    else:

        if (__tmp0['status'] == "successful"):
            status = 'was successful'
        else:
            status = 'failed'

        data = {
            "name": __tmp0['name'],
            "friendly_name": __tmp0['friendly_name'],
            "id": __tmp0['id'],
            "url": __tmp0['url'],
            "status": status
        }

        return ANSIBLETOWER_DEFAULT_MESSAGE_TEMPLATE.format(**data)

def __tmp2(hosts_data) -> str:
    hosts_data = sorted(hosts_data, key=operator.itemgetter('hostname'))
    hosts_content = ''
    for host in hosts_data:
        hosts_content += ANSIBLETOWER_JOB_HOST_ROW_TEMPLATE.format(
            hostname=host.get('hostname'),
            status=host.get('status')
        )
    return hosts_content
