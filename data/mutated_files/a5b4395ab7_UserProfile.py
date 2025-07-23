from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ1 : TypeAlias = "HttpResponse"
# Webhooks for external integrations.

from django.http import HttpRequest, HttpResponse

from zerver.decorator import api_key_only_webhook_view
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile

@api_key_only_webhook_view("Heroku", notify_bot_owner_on_invalid_json=False)
@has_request_variables
def api_heroku_webhook(request: __typ0, user_profile: <FILL>,
                       head: str=REQ(), app: str=REQ(), user: str=REQ(),
                       url: str=REQ(), git_log: str=REQ()) -> __typ1:
    template = "{} deployed version {} of [{}]({})\n``` quote\n{}\n```"
    content = template.format(user, head, app, url, git_log)

    check_send_webhook_message(request, user_profile, app, content)
    return json_success()
