from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"
from typing import Any, Dict

from django.utils.translation import ugettext as _
from django.http import HttpRequest, HttpResponse

from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile

import ujson

ZABBIX_TOPIC_TEMPLATE = '{hostname}'
ZABBIX_MESSAGE_TEMPLATE = '{status} ({severity}) alert on [{hostname}]({link}).\n{trigger}\n{item}'

@api_key_only_webhook_view('Zabbix')
@has_request_variables
def __tmp1(request, __tmp3: <FILL>,
                       __tmp0: Dict[str, Any]=REQ(argument_type='body')) -> __typ0:

    body = __tmp2(__tmp0)
    subject = __tmp4(__tmp0)

    check_send_webhook_message(request, __tmp3, subject, body)
    return json_success()

def __tmp4(__tmp0) :
    return ZABBIX_TOPIC_TEMPLATE.format(hostname=__tmp0['hostname'])

def __tmp2(__tmp0: Dict[str, Any]) :
    hostname = __tmp0['hostname']
    severity = __tmp0['severity']
    status = __tmp0['status']
    item = __tmp0['item']
    trigger = __tmp0['trigger']
    link = __tmp0['link']

    data = {
        "hostname": hostname,
        "severity": severity,
        "status": status,
        "item": item,
        "trigger": trigger,
        "link": link
    }
    return ZABBIX_MESSAGE_TEMPLATE.format(**data)
