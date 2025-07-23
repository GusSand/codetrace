from typing import Any, Dict, Optional, Tuple

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

def get_message_data(__tmp0: Dict[str, Any]) :
    link = "https://app.frontapp.com/open/" + __tmp0['target']['data']['id']
    outbox = __tmp0['conversation']['recipient']['handle']
    inbox = __tmp0['source']['data'][0]['address']
    subject = __tmp0['conversation']['subject']
    return link, outbox, inbox, subject

def get_source_name(__tmp0) :
    first_name = __tmp0['source']['data']['first_name']
    last_name = __tmp0['source']['data']['last_name']
    return "%s %s" % (first_name, last_name)

def get_target_name(__tmp0) -> str:
    first_name = __tmp0['target']['data']['first_name']
    last_name = __tmp0['target']['data']['last_name']
    return "%s %s" % (first_name, last_name)

def get_inbound_message_body(__tmp0: Dict[str, Any]) :
    link, outbox, inbox, subject = get_message_data(__tmp0)
    return "[Inbound message]({link}) from **{outbox}** to **{inbox}**.\n" \
           "```quote\n*Subject*: {subject}\n```" \
        .format(link=link, outbox=outbox, inbox=inbox, subject=subject)

def get_outbound_message_body(__tmp0) :
    link, outbox, inbox, subject = get_message_data(__tmp0)
    return "[Outbound message]({link}) from **{inbox}** to **{outbox}**.\n" \
           "```quote\n*Subject*: {subject}\n```" \
        .format(link=link, inbox=inbox, outbox=outbox, subject=subject)

def __tmp4(__tmp0) :
    link, outbox, inbox, subject = get_message_data(__tmp0)
    return "[Outbound reply]({link}) from **{inbox}** to **{outbox}**." \
        .format(link=link, inbox=inbox, outbox=outbox)

def get_comment_body(__tmp0: Dict[str, Any]) -> str:
    name = get_source_name(__tmp0)
    comment = __tmp0['target']['data']['body']
    return "**{name}** left a comment:\n```quote\n{comment}\n```" \
        .format(name=name, comment=comment)

def __tmp1(__tmp0) :
    source_name = get_source_name(__tmp0)
    target_name = get_target_name(__tmp0)

    if source_name == target_name:
        return "**{source_name}** assigned themselves." \
            .format(source_name=source_name)

    return "**{source_name}** assigned **{target_name}**." \
        .format(source_name=source_name, target_name=target_name)

def __tmp3(__tmp0) :
    name = get_source_name(__tmp0)
    return "Unassined by **{name}**.".format(name=name)

def get_conversation_archived_body(__tmp0) :
    name = get_source_name(__tmp0)
    return "Archived by **{name}**.".format(name=name)

def get_conversation_reopened_body(__tmp0) :
    name = get_source_name(__tmp0)
    return "Reopened by **{name}**.".format(name=name)

def get_conversation_deleted_body(__tmp0: Dict[str, Any]) :
    name = get_source_name(__tmp0)
    return "Deleted by **{name}**.".format(name=name)

def __tmp2(__tmp0) -> str:
    name = get_source_name(__tmp0)
    return "Restored by **{name}**.".format(name=name)

def get_conversation_tagged_body(__tmp0) :
    name = get_source_name(__tmp0)
    tag = __tmp0['target']['data']['name']
    return "**{name}** added tag **{tag}**.".format(name=name, tag=tag)

def get_conversation_untagged_body(__tmp0) -> str:
    name = get_source_name(__tmp0)
    tag = __tmp0['target']['data']['name']
    return "**{name}** removed tag **{tag}**.".format(name=name, tag=tag)

EVENT_FUNCTION_MAPPER = {
    'inbound': get_inbound_message_body,
    'outbound': get_outbound_message_body,
    'out_reply': __tmp4,
    'comment': get_comment_body,
    'mention': get_comment_body,
    'assign': __tmp1,
    'unassign': __tmp3,
    'archive': get_conversation_archived_body,
    'reopen': get_conversation_reopened_body,
    'trash': get_conversation_deleted_body,
    'restore': __tmp2,
    'tag': get_conversation_tagged_body,
    'untag': get_conversation_untagged_body
}

def get_body_based_on_event(event: str) :
    return EVENT_FUNCTION_MAPPER[event]

@api_key_only_webhook_view('Front')
@has_request_variables
def api_front_webhook(request: HttpRequest, user_profile: <FILL>,
                      __tmp0: Dict[str, Any]=REQ(argument_type='body')) :

    event = __tmp0['type']
    if event not in EVENT_FUNCTION_MAPPER:
        return json_error(_("Unknown webhook request"))

    topic = __tmp0['conversation']['id']
    body = get_body_based_on_event(event)(__tmp0)
    check_send_webhook_message(request, user_profile, topic, body)

    return json_success()
