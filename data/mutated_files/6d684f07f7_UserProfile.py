# Webhooks for external integrations.

import pprint
from typing import Any, Dict, Iterable, Optional

import ujson
from django.http import HttpRequest, HttpResponse

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import Client, UserProfile

PAGER_DUTY_EVENT_NAMES = {
    'incident.trigger': 'triggered',
    'incident.acknowledge': 'acknowledged',
    'incident.unacknowledge': 'unacknowledged',
    'incident.resolve': 'resolved',
    'incident.assign': 'assigned',
    'incident.escalate': 'escalated',
    'incident.delegate': 'delineated',
}

def __tmp4(message: Dict[str, Any]) -> Dict[str, Any]:
    # Normalize the message dict, after this all keys will exist. I would
    # rather some strange looking messages than dropping pages.

    __tmp0 = {}  # type: Dict[str, Any]
    __tmp0['action'] = PAGER_DUTY_EVENT_NAMES[message['type']]

    __tmp0['incident_id'] = message['data']['incident']['id']
    __tmp0['incident_num'] = message['data']['incident']['incident_number']
    __tmp0['incident_url'] = message['data']['incident']['html_url']

    __tmp0['service_name'] = message['data']['incident']['service']['name']
    __tmp0['service_url'] = message['data']['incident']['service']['html_url']

    # This key can be missing on null
    if message['data']['incident'].get('assigned_to_user', None):
        assigned_to_user = message['data']['incident']['assigned_to_user']
        __tmp0['assigned_to_email'] = assigned_to_user['email']
        __tmp0['assigned_to_username'] = assigned_to_user['email'].split('@')[0]
        __tmp0['assigned_to_url'] = assigned_to_user['html_url']
    else:
        __tmp0['assigned_to_email'] = 'nobody'
        __tmp0['assigned_to_username'] = 'nobody'
        __tmp0['assigned_to_url'] = ''

    # This key can be missing on null
    if message['data']['incident'].get('resolved_by_user', None):
        resolved_by_user = message['data']['incident']['resolved_by_user']
        __tmp0['resolved_by_email'] = resolved_by_user['email']
        __tmp0['resolved_by_username'] = resolved_by_user['email'].split('@')[0]
        __tmp0['resolved_by_url'] = resolved_by_user['html_url']
    else:
        __tmp0['resolved_by_email'] = 'nobody'
        __tmp0['resolved_by_username'] = 'nobody'
        __tmp0['resolved_by_url'] = ''

    trigger_message = []
    trigger_subject = message['data']['incident']['trigger_summary_data'].get('subject', '')
    if trigger_subject:
        trigger_message.append(trigger_subject)
    trigger_description = message['data']['incident']['trigger_summary_data'].get('description', '')
    if trigger_description:
        trigger_message.append(trigger_description)
    __tmp0['trigger_message'] = u'\n'.join(trigger_message)
    return __tmp0


def __tmp6(request: HttpRequest,
                            __tmp2: UserProfile,
                            message: Dict[str, Any]) :
    subject = 'pagerduty'
    body = (
        u'Unknown pagerduty message\n'
        u'```\n'
        u'%s\n'
        u'```') % (ujson.dumps(message, indent=2),)
    check_send_webhook_message(request, __tmp2, subject, body)


def __tmp3(request: HttpRequest,
                            __tmp2: <FILL>,
                            __tmp5: str,
                            __tmp0: Dict[str, Any]) -> None:
    if __tmp5 in ('incident.trigger', 'incident.unacknowledge'):
        template = (u':imp: Incident '
                    u'[{incident_num}]({incident_url}) {action} by '
                    u'[{service_name}]({service_url}) and assigned to '
                    u'[{assigned_to_username}@]({assigned_to_url})\n\n>{trigger_message}')

    elif __tmp5 == 'incident.resolve' and __tmp0['resolved_by_url']:
        template = (u':grinning: Incident '
                    u'[{incident_num}]({incident_url}) resolved by '
                    u'[{resolved_by_username}@]({resolved_by_url})\n\n>{trigger_message}')
    elif __tmp5 == 'incident.resolve' and not __tmp0['resolved_by_url']:
        template = (u':grinning: Incident '
                    u'[{incident_num}]({incident_url}) resolved\n\n>{trigger_message}')
    else:
        template = (u':no_good: Incident [{incident_num}]({incident_url}) '
                    u'{action} by [{assigned_to_username}@]({assigned_to_url})\n\n>{trigger_message}')

    subject = u'incident {incident_num}'.format(**__tmp0)
    body = template.format(**__tmp0)

    check_send_webhook_message(request, __tmp2, subject, body)


@api_key_only_webhook_view('PagerDuty')
@has_request_variables
def __tmp1(
        request: HttpRequest, __tmp2: UserProfile,
        payload: Dict[str, Iterable[Dict[str, Any]]]=REQ(argument_type='body'),
) -> HttpResponse:
    for message in payload['messages']:
        __tmp5 = message['type']

        if __tmp5 not in PAGER_DUTY_EVENT_NAMES:
            __tmp6(request, __tmp2, message)

        try:
            __tmp0 = __tmp4(message)
        except Exception:
            __tmp6(request, __tmp2, message)
        else:
            __tmp3(request, __tmp2, __tmp5, __tmp0)

    return json_success()
