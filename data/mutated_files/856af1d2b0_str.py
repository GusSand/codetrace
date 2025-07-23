from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "HttpRequest"
__typ1 : TypeAlias = "HttpResponse"
from typing import Any, Dict, Optional, Tuple

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

def __tmp17(__tmp13: Dict[str, __typ2]) -> Tuple[str, str, str, str]:
    link = "https://app.frontapp.com/open/" + __tmp13['target']['data']['id']
    outbox = __tmp13['conversation']['recipient']['handle']
    inbox = __tmp13['source']['data'][0]['address']
    subject = __tmp13['conversation']['subject']
    return link, outbox, inbox, subject

def __tmp6(__tmp13) :
    first_name = __tmp13['source']['data']['first_name']
    last_name = __tmp13['source']['data']['last_name']
    return "%s %s" % (first_name, last_name)

def __tmp14(__tmp13: Dict[str, __typ2]) -> str:
    first_name = __tmp13['target']['data']['first_name']
    last_name = __tmp13['target']['data']['last_name']
    return "%s %s" % (first_name, last_name)

def __tmp12(__tmp13: Dict[str, __typ2]) -> str:
    link, outbox, inbox, subject = __tmp17(__tmp13)
    return "[Inbound message]({link}) from **{outbox}** to **{inbox}**.\n" \
           "```quote\n*Subject*: {subject}\n```" \
        .format(link=link, outbox=outbox, inbox=inbox, subject=subject)

def __tmp15(__tmp13: Dict[str, __typ2]) -> str:
    link, outbox, inbox, subject = __tmp17(__tmp13)
    return "[Outbound message]({link}) from **{inbox}** to **{outbox}**.\n" \
           "```quote\n*Subject*: {subject}\n```" \
        .format(link=link, inbox=inbox, outbox=outbox, subject=subject)

def __tmp18(__tmp13: Dict[str, __typ2]) :
    link, outbox, inbox, subject = __tmp17(__tmp13)
    return "[Outbound reply]({link}) from **{inbox}** to **{outbox}**." \
        .format(link=link, inbox=inbox, outbox=outbox)

def __tmp1(__tmp13: Dict[str, __typ2]) -> str:
    name = __tmp6(__tmp13)
    comment = __tmp13['target']['data']['body']
    return "**{name}** left a comment:\n```quote\n{comment}\n```" \
        .format(name=name, comment=comment)

def __tmp9(__tmp13: Dict[str, __typ2]) -> str:
    source_name = __tmp6(__tmp13)
    target_name = __tmp14(__tmp13)

    if source_name == target_name:
        return "**{source_name}** assigned themselves." \
            .format(source_name=source_name)

    return "**{source_name}** assigned **{target_name}**." \
        .format(source_name=source_name, target_name=target_name)

def __tmp8(__tmp13: Dict[str, __typ2]) -> str:
    name = __tmp6(__tmp13)
    return "Unassined by **{name}**.".format(name=name)

def __tmp10(__tmp13: Dict[str, __typ2]) -> str:
    name = __tmp6(__tmp13)
    return "Archived by **{name}**.".format(name=name)

def __tmp7(__tmp13: Dict[str, __typ2]) :
    name = __tmp6(__tmp13)
    return "Reopened by **{name}**.".format(name=name)

def __tmp16(__tmp13: Dict[str, __typ2]) -> str:
    name = __tmp6(__tmp13)
    return "Deleted by **{name}**.".format(name=name)

def get_conversation_restored_body(__tmp13: Dict[str, __typ2]) -> str:
    name = __tmp6(__tmp13)
    return "Restored by **{name}**.".format(name=name)

def __tmp3(__tmp13: Dict[str, __typ2]) :
    name = __tmp6(__tmp13)
    tag = __tmp13['target']['data']['name']
    return "**{name}** added tag **{tag}**.".format(name=name, tag=tag)

def __tmp4(__tmp13: Dict[str, __typ2]) -> str:
    name = __tmp6(__tmp13)
    tag = __tmp13['target']['data']['name']
    return "**{name}** removed tag **{tag}**.".format(name=name, tag=tag)

EVENT_FUNCTION_MAPPER = {
    'inbound': __tmp12,
    'outbound': __tmp15,
    'out_reply': __tmp18,
    'comment': __tmp1,
    'mention': __tmp1,
    'assign': __tmp9,
    'unassign': __tmp8,
    'archive': __tmp10,
    'reopen': __tmp7,
    'trash': __tmp16,
    'restore': get_conversation_restored_body,
    'tag': __tmp3,
    'untag': __tmp4
}

def __tmp11(__tmp5: <FILL>) -> __typ2:
    return EVENT_FUNCTION_MAPPER[__tmp5]

@api_key_only_webhook_view('Front')
@has_request_variables
def __tmp2(request: __typ0, __tmp0: UserProfile,
                      __tmp13: Dict[str, __typ2]=REQ(argument_type='body')) -> __typ1:

    __tmp5 = __tmp13['type']
    if __tmp5 not in EVENT_FUNCTION_MAPPER:
        return json_error(_("Unknown webhook request"))

    topic = __tmp13['conversation']['id']
    body = __tmp11(__tmp5)(__tmp13)
    check_send_webhook_message(request, __tmp0, topic, body)

    return json_success()
