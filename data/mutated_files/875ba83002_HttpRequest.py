from typing import TypeAlias
__typ1 : TypeAlias = "str"
from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

GCI_MESSAGE_TEMPLATE = u'**{actor}** {action} the task [{task_name}]({task_url}).'
GCI_TOPIC_TEMPLATE = u'{student_name}'


def build_instance_url(instance_id) :
    return "https://codein.withgoogle.com/dashboard/task-instances/{}/".format(instance_id)

class __typ0(Exception):
    pass

def get_abandon_event_body(__tmp0: Dict[__typ1, Any]) -> __typ1:
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['task_claimed_by'],
        action='{}ed'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def __tmp4(__tmp0: Dict[__typ1, Any]) :
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['task_claimed_by'],
        action='{}ted'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def get_comment_event_body(__tmp0) -> __typ1:
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['author'],
        action='{}ed on'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def get_claim_event_body(__tmp0: Dict[__typ1, Any]) :
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['task_claimed_by'],
        action='{}ed'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def __tmp2(__tmp0) -> __typ1:
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['author'],
        action='{}d'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def get_approve_pending_pc_event_body(__tmp0: Dict[__typ1, Any]) -> __typ1:
    template = "{} (pending parental consent).".format(GCI_MESSAGE_TEMPLATE.rstrip('.'))
    return template.format(
        actor=__tmp0['author'],
        action='approved',
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def get_needswork_event_body(__tmp0) -> __typ1:
    template = "{} for more work.".format(GCI_MESSAGE_TEMPLATE.rstrip('.'))
    return template.format(
        actor=__tmp0['author'],
        action='submitted',
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def get_extend_event_body(__tmp0) :
    template = "{} by {days} day(s).".format(GCI_MESSAGE_TEMPLATE.rstrip('.'),
                                             days=__tmp0['extension_days'])
    return template.format(
        actor=__tmp0['author'],
        action='extended the deadline for',
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def get_unassign_event_body(__tmp0) :
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['author'],
        action='unassigned **{student}** from'.format(student=__tmp0['task_claimed_by']),
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

def __tmp1(__tmp0) -> __typ1:
    return u'The deadline for the task [{task_name}]({task_url}) has passed.'.format(
        task_name=__tmp0['task_definition_name'],
        task_url=build_instance_url(__tmp0['task_instance']),
    )

@api_key_only_webhook_view("Google-Code-In")
@has_request_variables
def api_gci_webhook(request: <FILL>, user_profile: UserProfile,
                    __tmp0: Dict[__typ1, Any]=REQ(argument_type='body')) :
    __tmp3 = __tmp5(__tmp0)
    if __tmp3 is not None:
        body = get_body_based_on_event(__tmp3)(__tmp0)
        subject = GCI_TOPIC_TEMPLATE.format(
            student_name=__tmp0['task_claimed_by']
        )
        check_send_webhook_message(request, user_profile, subject, body)

    return json_success()

EVENTS_FUNCTION_MAPPER = {
    'abandon': get_abandon_event_body,
    'approve': __tmp2,
    'approve-pending-pc': get_approve_pending_pc_event_body,
    'claim': get_claim_event_body,
    'comment': get_comment_event_body,
    'extend': get_extend_event_body,
    'needswork': get_needswork_event_body,
    'outoftime': __tmp1,
    'submit': __tmp4,
    'unassign': get_unassign_event_body,
}

def __tmp5(__tmp0: Dict[__typ1, Any]) -> Optional[__typ1]:
    __tmp3 = __tmp0['event_type']
    if __tmp3 in EVENTS_FUNCTION_MAPPER:
        return __tmp3

    raise __typ0(u"Event '{}' is unknown and cannot be handled".format(__tmp3))  # nocoverage

def get_body_based_on_event(__tmp3: __typ1) :
    return EVENTS_FUNCTION_MAPPER[__tmp3]
