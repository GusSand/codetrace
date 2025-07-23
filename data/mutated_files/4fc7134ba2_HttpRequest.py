from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "str"
# Webhooks pfor external integrations.
from typing import Any, Dict

import ujson
from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message, \
    UnexpectedWebhookEventType
from zerver.models import UserProfile

PINGDOM_TOPIC_TEMPLATE = '{name} status.'
PINGDOM_MESSAGE_TEMPLATE = ('Service {service_url} changed its {type} status'
                            ' from {previous_state} to {current_state}.')
PINGDOM_MESSAGE_DESCRIPTION_TEMPLATE = 'Description: {description}.'


SUPPORTED_CHECK_TYPES = (
    'HTTP',
    'HTTP_CUSTOM'
    'HTTPS',
    'SMTP',
    'POP3',
    'IMAP',
    'PING',
    'DNS',
    'UDP',
    'PORT_TCP',
)


@api_key_only_webhook_view('Pingdom')
@has_request_variables
def api_pingdom_webhook(request: <FILL>, __tmp1: __typ1,
                        __tmp0: Dict[__typ0, Any]=REQ(argument_type='body')) :
    check_type = get_check_type(__tmp0)

    if check_type in SUPPORTED_CHECK_TYPES:
        subject = get_subject_for_http_request(__tmp0)
        body = get_body_for_http_request(__tmp0)
    else:
        raise UnexpectedWebhookEventType('Pingdom', check_type)

    check_send_webhook_message(request, __tmp1, subject, body)
    return json_success()


def get_subject_for_http_request(__tmp0: Dict[__typ0, Any]) -> __typ0:
    return PINGDOM_TOPIC_TEMPLATE.format(name=__tmp0['check_name'])


def get_body_for_http_request(__tmp0) -> __typ0:
    current_state = __tmp0['current_state']
    previous_state = __tmp0['previous_state']

    data = {
        'service_url': __tmp0['check_params']['hostname'],
        'previous_state': previous_state,
        'current_state': current_state,
        'type': get_check_type(__tmp0)
    }
    body = PINGDOM_MESSAGE_TEMPLATE.format(**data)
    if current_state == 'DOWN' and previous_state == 'UP':
        description = PINGDOM_MESSAGE_DESCRIPTION_TEMPLATE.format(description=__tmp0['long_description'])
        body += '\n{description}'.format(description=description)
    return body


def get_check_type(__tmp0) :
    return __tmp0['check_type']
