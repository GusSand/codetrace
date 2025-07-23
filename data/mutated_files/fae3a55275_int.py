from typing import TypeAlias
__typ2 : TypeAlias = "HttpResponse"
__typ1 : TypeAlias = "HttpRequest"
__typ3 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "str"
# Webhooks for external integrations.

from django.http import HttpRequest, HttpResponse

from zerver.decorator import authenticated_rest_api_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile, get_client

def truncate(string, __tmp0: <FILL>) -> __typ0:
    if len(string) > __tmp0:
        string = string[:__tmp0-3] + '...'
    return string

@authenticated_rest_api_view(webhook_client_name="Zendesk")
@has_request_variables
def api_zendesk_webhook(request, user_profile,
                        ticket_title: __typ0=REQ(), ticket_id: __typ0=REQ(),
                        message: __typ0=REQ()) :
    """
    Zendesk uses trigers with message templates. This webhook uses the
    ticket_id and ticket_title to create a subject. And passes with zendesk
    user's configured message to zulip.
    """
    subject = truncate('#%s: %s' % (ticket_id, ticket_title), 60)
    check_send_webhook_message(request, user_profile, subject, message)
    return json_success()
