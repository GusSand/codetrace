from typing import TypeAlias
__typ1 : TypeAlias = "Any"
from typing import Any, Dict, Optional

from django.http import HttpRequest, HttpResponse

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

GCI_MESSAGE_TEMPLATE = u'**{actor}** {action} the task [{task_name}]({task_url}).'
GCI_TOPIC_TEMPLATE = u'{student_name}'


def __tmp14(__tmp10) :
    return "https://codein.withgoogle.com/dashboard/task-instances/{}/".format(__tmp10)

class __typ0(Exception):
    pass

def __tmp15(__tmp0) :
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['task_claimed_by'],
        action='{}ed'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp11(__tmp0: Dict[str, __typ1]) -> str:
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['task_claimed_by'],
        action='{}ted'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp12(__tmp0: Dict[str, __typ1]) :
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['author'],
        action='{}ed on'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp9(__tmp0: Dict[str, __typ1]) -> str:
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['task_claimed_by'],
        action='{}ed'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp5(__tmp0: Dict[str, __typ1]) :
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['author'],
        action='{}d'.format(__tmp0['event_type']),
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp16(__tmp0) :
    template = "{} (pending parental consent).".format(GCI_MESSAGE_TEMPLATE.rstrip('.'))
    return template.format(
        actor=__tmp0['author'],
        action='approved',
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp2(__tmp0) :
    template = "{} for more work.".format(GCI_MESSAGE_TEMPLATE.rstrip('.'))
    return template.format(
        actor=__tmp0['author'],
        action='submitted',
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp1(__tmp0) :
    template = "{} by {days} day(s).".format(GCI_MESSAGE_TEMPLATE.rstrip('.'),
                                             days=__tmp0['extension_days'])
    return template.format(
        actor=__tmp0['author'],
        action='extended the deadline for',
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def __tmp13(__tmp0: Dict[str, __typ1]) -> str:
    return GCI_MESSAGE_TEMPLATE.format(
        actor=__tmp0['author'],
        action='unassigned **{student}** from'.format(student=__tmp0['task_claimed_by']),
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

def get_outoftime_event_body(__tmp0) :
    return u'The deadline for the task [{task_name}]({task_url}) has passed.'.format(
        task_name=__tmp0['task_definition_name'],
        task_url=__tmp14(__tmp0['task_instance']),
    )

@api_key_only_webhook_view("Google-Code-In")
@has_request_variables
def __tmp8(request, __tmp7: UserProfile,
                    __tmp0: Dict[str, __typ1]=REQ(argument_type='body')) -> HttpResponse:
    __tmp4 = __tmp3(__tmp0)
    if __tmp4 is not None:
        body = __tmp6(__tmp4)(__tmp0)
        subject = GCI_TOPIC_TEMPLATE.format(
            student_name=__tmp0['task_claimed_by']
        )
        check_send_webhook_message(request, __tmp7, subject, body)

    return json_success()

EVENTS_FUNCTION_MAPPER = {
    'abandon': __tmp15,
    'approve': __tmp5,
    'approve-pending-pc': __tmp16,
    'claim': __tmp9,
    'comment': __tmp12,
    'extend': __tmp1,
    'needswork': __tmp2,
    'outoftime': get_outoftime_event_body,
    'submit': __tmp11,
    'unassign': __tmp13,
}

def __tmp3(__tmp0: Dict[str, __typ1]) -> Optional[str]:
    __tmp4 = __tmp0['event_type']
    if __tmp4 in EVENTS_FUNCTION_MAPPER:
        return __tmp4

    raise __typ0(u"Event '{}' is unknown and cannot be handled".format(__tmp4))  # nocoverage

def __tmp6(__tmp4: <FILL>) :
    return EVENTS_FUNCTION_MAPPER[__tmp4]
