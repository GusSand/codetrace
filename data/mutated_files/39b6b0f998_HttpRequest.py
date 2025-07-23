from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"

from django.http import HttpRequest, HttpResponse

from zerver.decorator import human_users_only
from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success
from zerver.lib.validator import check_string
from zerver.models import UserProfile

@human_users_only
@has_request_variables
def set_tutorial_status(request: <FILL>, __tmp0: UserProfile,
                        status: str=REQ(validator=check_string)) :
    if status == 'started':
        __tmp0.tutorial_status = UserProfile.TUTORIAL_STARTED
    elif status == 'finished':
        __tmp0.tutorial_status = UserProfile.TUTORIAL_FINISHED
    __tmp0.save(update_fields=["tutorial_status"])

    return json_success()
