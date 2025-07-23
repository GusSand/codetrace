from typing import TypeAlias
__typ2 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
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

def __tmp0(request: __typ2, __tmp4: UserProfile,
                           __tmp1) -> None:
    event_type = get_event_type(__tmp1)
    subject = TOPIC_TEMPLATE.format(service_url=__tmp1['check']['url'])
    body = EVENT_TYPE_BODY_MAPPER[event_type](__tmp1)
    check_send_webhook_message(request, __tmp4, subject, body)

def get_body_for_up_event(__tmp1: Dict[__typ1, Any]) -> __typ1:
    body = "Service is `up`"
    event_downtime = __tmp1['downtime']
    if event_downtime['started_at']:
        body = "{} again".format(body)
        string_date = get_time_string_based_on_duration(event_downtime['duration'])
        if string_date:
            body = "{} after {}".format(body, string_date)
    return "{}.".format(body)

def get_time_string_based_on_duration(__tmp5) -> __typ1:
    days, reminder = divmod(__tmp5, 86400)
    hours, reminder = divmod(reminder, 3600)
    minutes, seconds = divmod(reminder, 60)

    string_date = ''
    string_date += __tmp3(days, 'day')
    string_date += __tmp3(hours, 'hour')
    string_date += __tmp3(minutes, 'minute')
    string_date += __tmp3(seconds, 'second')
    return string_date.rstrip()

def __tmp3(value: __typ0, __tmp2) -> __typ1:
    if value == 1:
        return "1 {} ".format(__tmp2)
    if value > 1:
        return "{} {}s ".format(value, __tmp2)
    return ''

def __tmp7(__tmp1: Dict[__typ1, Any]) -> __typ1:
    return "Service is `down`. It returned a {} error at {}.".format(
        __tmp1['downtime']['error'],
        __tmp1['downtime']['started_at'].replace('T', ' ').replace('Z', ' UTC'))

@api_key_only_webhook_view('Updown')
@has_request_variables
def __tmp6(
        request, __tmp4: <FILL>,
        payload: List[Dict[__typ1, Any]]=REQ(argument_type='body')
) -> HttpResponse:
    for __tmp1 in payload:
        __tmp0(request, __tmp4, __tmp1)
    return json_success()

EVENT_TYPE_BODY_MAPPER = {
    'up': get_body_for_up_event,
    'down': __tmp7
}

def get_event_type(__tmp1: Dict[__typ1, Any]) -> __typ1:
    event_type_match = re.match('check.(.*)', __tmp1['event'])
    if event_type_match:
        event_type = event_type_match.group(1)
        if event_type in EVENT_TYPE_BODY_MAPPER:
            return event_type
    raise UnexpectedWebhookEventType('Updown', __tmp1['event'])
