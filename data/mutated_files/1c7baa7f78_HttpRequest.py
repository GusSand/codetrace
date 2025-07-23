from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"
# Webhooks for external integrations.
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile
from django.http import HttpRequest, HttpResponse
from typing import Dict, Any

CHECK_IS_REPLY = "in reply to"

@api_key_only_webhook_view('Flock')
@has_request_variables
def __tmp0(request: <FILL>, user_profile,
                      payload: Dict[str, Any]=REQ(argument_type='body')) :

    if len(payload["text"]) != 0:
        message_body = payload["text"]
    else:
        message_body = payload["notification"]

    topic = 'Flock notifications'
    body = u"{}".format(message_body)

    check_send_webhook_message(request, user_profile, topic, body)

    return json_success()
