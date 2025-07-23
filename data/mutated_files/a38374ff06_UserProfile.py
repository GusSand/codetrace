from typing import TypeAlias
__typ3 : TypeAlias = "HttpResponse"
__typ2 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
# Webhooks for external integrations.

from django.http import HttpRequest, HttpResponse

from zerver.decorator import authenticated_rest_api_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile, get_client

def truncate(__tmp0: __typ1, __tmp1: __typ0) -> __typ1:
    if len(__tmp0) > __tmp1:
        __tmp0 = __tmp0[:__tmp1-3] + '...'
    return __tmp0

@authenticated_rest_api_view(webhook_client_name="Zendesk")
@has_request_variables
def __tmp3(request: __typ2, __tmp2: <FILL>,
                        ticket_title: __typ1=REQ(), ticket_id: __typ1=REQ(),
                        message: __typ1=REQ()) :
    """
    Zendesk uses trigers with message templates. This webhook uses the
    ticket_id and ticket_title to create a subject. And passes with zendesk
    user's configured message to zulip.
    """
    subject = truncate('#%s: %s' % (ticket_id, ticket_title), 60)
    check_send_webhook_message(request, __tmp2, subject, message)
    return json_success()
