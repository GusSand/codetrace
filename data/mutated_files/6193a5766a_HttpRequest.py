from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "str"
# Webhooks for external integrations.
import re
from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

@api_key_only_webhook_view("AppFollow")
@has_request_variables
def api_appfollow_webhook(request: <FILL>, __tmp0: __typ1,
                          payload: Dict[__typ0, Any]=REQ(argument_type="body")) -> __typ2:
    message = payload["text"]
    app_name_search = re.search(r'\A(.+)', message)
    assert app_name_search is not None
    app_name = app_name_search.group(0)
    topic = app_name

    check_send_webhook_message(request, __tmp0, topic,
                               body=__tmp1(message))
    return json_success()

def __tmp1(text: __typ0) :
    # Converts Slack-style markdown to Zulip format
    # Implemented mainly for AppFollow messages
    # Not ready for general use as some edge-cases not handled
    # Convert Bold
    text = re.sub(r'(?:(?<=\s)|(?<=^))\*(.+?\S)\*(?=\s|$)', r'**\1**', text)
    # Convert Italics
    text = re.sub(r'\b_(\s*)(.+?)(\s*)_\b', r'\1*\2*\3', text)
    # Convert Strikethrough
    text = re.sub(r'(?:(?<=\s)|(?<=^))~(.+?\S)~(?=\s|$)', r'~~\1~~', text)

    return text
