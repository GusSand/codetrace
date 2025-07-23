from typing import TypeAlias
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

def send_message_for_event(request: HttpRequest, __tmp4: UserProfile,
                           __tmp1) -> None:
    event_type = get_event_type(__tmp1)
    subject = TOPIC_TEMPLATE.format(service_url=__tmp1['check']['url'])
    body = EVENT_TYPE_BODY_MAPPER[event_type](__tmp1)
    check_send_webhook_message(request, __tmp4, subject, body)

def __tmp0(__tmp1: Dict[__typ1, Any]) -> __typ1:
    body = "Service is `up`"
    event_downtime = __tmp1['downtime']
    if event_downtime['started_at']:
        body = "{} again".format(body)
        string_date = get_time_string_based_on_duration(event_downtime['duration'])
        if string_date:
            body = "{} after {}".format(body, string_date)
    return "{}.".format(body)

def get_time_string_based_on_duration(duration) -> __typ1:
    days, reminder = divmod(duration, 86400)
    hours, reminder = divmod(reminder, 3600)
    minutes, seconds = divmod(reminder, 60)

    string_date = ''
    string_date += add_time_part_to_string_date_if_needed(days, 'day')
    string_date += add_time_part_to_string_date_if_needed(hours, 'hour')
    string_date += add_time_part_to_string_date_if_needed(minutes, 'minute')
    string_date += add_time_part_to_string_date_if_needed(seconds, 'second')
    return string_date.rstrip()

def add_time_part_to_string_date_if_needed(__tmp2: __typ0, __tmp3: __typ1) -> __typ1:
    if __tmp2 == 1:
        return "1 {} ".format(__tmp3)
    if __tmp2 > 1:
        return "{} {}s ".format(__tmp2, __tmp3)
    return ''

def __tmp6(__tmp1: Dict[__typ1, Any]) -> __typ1:
    return "Service is `down`. It returned a {} error at {}.".format(
        __tmp1['downtime']['error'],
        __tmp1['downtime']['started_at'].replace('T', ' ').replace('Z', ' UTC'))

@api_key_only_webhook_view('Updown')
@has_request_variables
def __tmp5(
        request: <FILL>, __tmp4: UserProfile,
        payload: List[Dict[__typ1, Any]]=REQ(argument_type='body')
) -> HttpResponse:
    for __tmp1 in payload:
        send_message_for_event(request, __tmp4, __tmp1)
    return json_success()

EVENT_TYPE_BODY_MAPPER = {
    'up': __tmp0,
    'down': __tmp6
}

def get_event_type(__tmp1: Dict[__typ1, Any]) -> __typ1:
    event_type_match = re.match('check.(.*)', __tmp1['event'])
    if event_type_match:
        event_type = event_type_match.group(1)
        if event_type in EVENT_TYPE_BODY_MAPPER:
            return event_type
    raise UnexpectedWebhookEventType('Updown', __tmp1['event'])
