from typing import TypeAlias
__typ1 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "str"
# Webhooks for external integrations.
from django.utils.translation import ugettext as _
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import get_client, UserProfile
from django.http import HttpRequest, HttpResponse
from typing import Dict, Any

INCIDENT_TEMPLATE = u'**{name}** \n * State: **{state}** \n * Description: {content}'
COMPONENT_TEMPLATE = u'**{name}** has changed status from **{old_status}** to **{new_status}**'
TOPIC_TEMPLATE = u'{name}: {description}'

def __tmp2(__tmp0) -> __typ0:
    return INCIDENT_TEMPLATE.format(
        name = __tmp0["incident"]["name"],
        state = __tmp0["incident"]["status"],
        content = __tmp0["incident"]["incident_updates"][0]["body"],
    )

def __tmp4(__tmp0) :
    return COMPONENT_TEMPLATE.format(
        name = __tmp0["component"]["name"],
        old_status = __tmp0["component_update"]["old_status"],
        new_status = __tmp0["component_update"]["new_status"],
    )

def __tmp3(__tmp0) :
    return TOPIC_TEMPLATE.format(
        name = __tmp0["incident"]["name"],
        description = __tmp0["page"]["status_description"],
    )

def __tmp5(__tmp0) :
    return TOPIC_TEMPLATE.format(
        name = __tmp0["component"]["name"],
        description = __tmp0["page"]["status_description"],
    )

@api_key_only_webhook_view('Statuspage')
@has_request_variables
def __tmp6(request: HttpRequest, __tmp1: <FILL>,
                           __tmp0: Dict[__typ0, Any]=REQ(argument_type='body')) :

    status = __tmp0["page"]["status_indicator"]

    if status == "none":
        topic = __tmp3(__tmp0)
        body = __tmp2(__tmp0)
    else:
        topic = __tmp5(__tmp0)
        body = __tmp4(__tmp0)

    check_send_webhook_message(request, __tmp1, topic, body)
    return json_success()
