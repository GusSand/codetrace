from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"
from django.http import HttpRequest, HttpResponse
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.models import UserProfile

@api_key_only_webhook_view('Dropbox', notify_bot_owner_on_invalid_json=False)
@has_request_variables
def __tmp1(request, __tmp0: <FILL>) :
    if request.method == 'GET':
        return __typ0(request.GET['challenge'])
    elif request.method == 'POST':
        topic = 'Dropbox'
        check_send_webhook_message(request, __tmp0, topic,
                                   "File has been updated on Dropbox!")
        return json_success()
