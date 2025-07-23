from typing import TypeAlias
__typ0 : TypeAlias = "str"
from typing import Any, Dict

from django.utils.translation import ugettext as _
from django.http import HttpRequest, HttpResponse

from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile

import ujson

APPVEYOR_TOPIC_TEMPLATE = '{project_name}'
APPVEYOR_MESSAGE_TEMPLATE = ('[Build {project_name} {build_version} {status}]({build_url})\n'
                             'Commit [{commit_id}]({commit_url}) by {committer_name}'
                             ' on {commit_date}: {commit_message}\n'
                             'Build Started: {started}\n'
                             'Build Finished: {finished}')

@api_key_only_webhook_view('Appveyor')
@has_request_variables
def __tmp4(request: <FILL>, __tmp2: UserProfile,
                         __tmp0: Dict[__typ0, Any]=REQ(argument_type='body')) :

    body = __tmp1(__tmp0)
    subject = __tmp3(__tmp0)

    check_send_webhook_message(request, __tmp2, subject, body)
    return json_success()

def __tmp3(__tmp0) :
    event_data = __tmp0['eventData']
    return APPVEYOR_TOPIC_TEMPLATE.format(project_name=event_data['projectName'])

def __tmp1(__tmp0: Dict[__typ0, Any]) :
    event_data = __tmp0['eventData']

    data = {
        "project_name": event_data['projectName'],
        "build_version": event_data['buildVersion'],
        "status": event_data['status'],
        "build_url": event_data['buildUrl'],
        "commit_url": event_data['commitUrl'],
        "committer_name": event_data['committerName'],
        "commit_date": event_data['commitDate'],
        "commit_message": event_data['commitMessage'],
        "commit_id": event_data['commitId'],
        "started": event_data['started'],
        "finished": event_data['finished']
    }
    return APPVEYOR_MESSAGE_TEMPLATE.format(**data)
