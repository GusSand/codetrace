from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"

from django.http import HttpRequest, HttpResponse
from typing import List

from zerver.decorator import has_request_variables, REQ, JsonableError
from zerver.lib.actions import check_send_typing_notification, \
    extract_recipients
from zerver.lib.response import json_success
from zerver.models import UserProfile

@has_request_variables
def __tmp1(
        request: <FILL>, __tmp0,
        operator: str=REQ('op'),
        notification_to: List[str]=REQ('to', converter=extract_recipients, default=[]),
) :
    check_send_typing_notification(__tmp0, notification_to, operator)
    return json_success()
