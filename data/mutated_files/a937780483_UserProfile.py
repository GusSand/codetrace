from typing import TypeAlias
__typ2 : TypeAlias = "HttpResponse"
__typ1 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "str"
# Webhooks for external integrations.
from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.models import UserProfile

AIRBRAKE_TOPIC_TEMPLATE = '{project_name}'
AIRBRAKE_MESSAGE_TEMPLATE = '[{error_class}]({error_url}): "{error_message}" occurred.'

@api_key_only_webhook_view('Airbrake')
@has_request_variables
def __tmp3(request, user_profile: <FILL>,
                         __tmp0: Dict[__typ0, Any]=REQ(argument_type='body')) :
    subject = __tmp2(__tmp0)
    body = __tmp1(__tmp0)
    check_send_webhook_message(request, user_profile, subject, body)
    return json_success()

def __tmp2(__tmp0) :
    return AIRBRAKE_TOPIC_TEMPLATE.format(project_name=__tmp0['error']['project']['name'])

def __tmp1(__tmp0) :
    data = {
        'error_url': __tmp0['airbrake_error_url'],
        'error_class': __tmp0['error']['error_class'],
        'error_message': __tmp0['error']['error_message'],
    }
    return AIRBRAKE_MESSAGE_TEMPLATE.format(**data)
