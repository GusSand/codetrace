from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ1 : TypeAlias = "HttpResponse"
# Webhooks for external integrations.

from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import Client, UserProfile

@api_key_only_webhook_view('SolanoLabs')
@has_request_variables
def api_solano_webhook(request: __typ0, __tmp0,
                       payload: Dict[str, Any]=REQ(argument_type='body')) -> __typ1:
    event = payload.get('event')
    __tmp2 = 'build update'
    if event == 'test':
        return __tmp1(request, __tmp0, __tmp2)
    try:
        author = payload['committers'][0]
    except KeyError:
        author = 'Unknown'
    status = payload['status']
    build_log = payload['url']
    repository = payload['repository']['url']
    commit_id = payload['commit_id']

    good_status = ['passed']
    bad_status  = ['failed', 'error']
    neutral_status = ['running']
    emoji = ''
    if status in good_status:
        emoji = ':thumbs_up:'
    elif status in bad_status:
        emoji = ':thumbs_down:'
    elif status in neutral_status:
        emoji = ':arrows_counterclockwise:'
    else:
        emoji = "(No emoji specified for status '%s'.)" % (status,)

    template = (
        u'Author: {}\n'
        u'Commit: [{}]({})\n'
        u'Build status: {} {}\n'
        u'[Build Log]({})')

    # If the service is not one of the following, the url is of the repository home, not the individual
    # commit itself.
    commit_url = repository.split('@')[1]
    if 'github' in repository:
        commit_url += '/commit/{}'.format(commit_id)
    elif 'bitbucket' in repository:
        commit_url += '/commits/{}'.format(commit_id)
    elif 'gitlab' in repository:
        commit_url += '/pipelines/{}'.format(commit_id)

    body = template.format(author, commit_id, commit_url, status, emoji, build_log)

    check_send_webhook_message(request, __tmp0, __tmp2, body)
    return json_success()

def __tmp1(request: __typ0, __tmp0: <FILL>,
                      __tmp2: str) -> __typ1:
    body = 'Solano webhook set up correctly'
    check_send_webhook_message(request, __tmp0, __tmp2, body)
    return json_success()
