from typing import TypeAlias
__typ2 : TypeAlias = "HttpResponse"
__typ1 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "str"
# Webhooks for external integrations.
import re
from datetime import datetime
from typing import Any, Dict, List

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.exceptions import JsonableError
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message, \
    UnexpectedWebhookEventType
from zerver.models import Client, UserProfile

TOPIC_TEMPLATE = "{service_url}"

def send_message_for_event(request, __tmp3: UserProfile,
                           __tmp2: Dict[__typ0, Any]) :
    event_type = __tmp4(__tmp2)
    subject = TOPIC_TEMPLATE.format(service_url=__tmp2['check']['url'])
    body = EVENT_TYPE_BODY_MAPPER[event_type](__tmp2)
    check_send_webhook_message(request, __tmp3, subject, body)

def get_body_for_up_event(__tmp2) -> __typ0:
    body = "Service is `up`"
    event_downtime = __tmp2['downtime']
    if event_downtime['started_at']:
        body = "{} again".format(body)
        string_date = __tmp5(event_downtime['duration'])
        if string_date:
            body = "{} after {}".format(body, string_date)
    return "{}.".format(body)

def __tmp5(__tmp1) :
    days, reminder = divmod(__tmp1, 86400)
    hours, reminder = divmod(reminder, 3600)
    minutes, seconds = divmod(reminder, 60)

    string_date = ''
    string_date += __tmp0(days, 'day')
    string_date += __tmp0(hours, 'hour')
    string_date += __tmp0(minutes, 'minute')
    string_date += __tmp0(seconds, 'second')
    return string_date.rstrip()

def __tmp0(value: <FILL>, text_name) -> __typ0:
    if value == 1:
        return "1 {} ".format(text_name)
    if value > 1:
        return "{} {}s ".format(value, text_name)
    return ''

def get_body_for_down_event(__tmp2) -> __typ0:
    return "Service is `down`. It returned a {} error at {}.".format(
        __tmp2['downtime']['error'],
        __tmp2['downtime']['started_at'].replace('T', ' ').replace('Z', ' UTC'))

@api_key_only_webhook_view('Updown')
@has_request_variables
def api_updown_webhook(
        request: __typ1, __tmp3,
        payload: List[Dict[__typ0, Any]]=REQ(argument_type='body')
) -> __typ2:
    for __tmp2 in payload:
        send_message_for_event(request, __tmp3, __tmp2)
    return json_success()

EVENT_TYPE_BODY_MAPPER = {
    'up': get_body_for_up_event,
    'down': get_body_for_down_event
}

def __tmp4(__tmp2: Dict[__typ0, Any]) :
    event_type_match = re.match('check.(.*)', __tmp2['event'])
    if event_type_match:
        event_type = event_type_match.group(1)
        if event_type in EVENT_TYPE_BODY_MAPPER:
            return event_type
    raise UnexpectedWebhookEventType('Updown', __tmp2['event'])
