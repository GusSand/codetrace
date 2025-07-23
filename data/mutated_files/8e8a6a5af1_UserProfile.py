from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"
from typing import Any, Callable, Dict

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

@api_key_only_webhook_view('IFTTT')
@has_request_variables
def __tmp1(request: HttpRequest, __tmp0: <FILL>,
                         payload: Dict[str, Any]=REQ(argument_type='body')) :
    topic = payload.get('topic')
    content = payload.get('content')

    if topic is None:
        topic = payload.get('subject')  # Backwards-compatibility
        if topic is None:
            return json_error(_("Topic can't be empty"))

    if content is None:
        return json_error(_("Content can't be empty"))

    check_send_webhook_message(request, __tmp0, topic, content)
    return json_success()
