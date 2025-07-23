from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ1 : TypeAlias = "HttpResponse"

from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import to_non_negative_int
from zerver.lib.actions import do_update_pointer
from zerver.lib.request import has_request_variables, JsonableError, REQ
from zerver.lib.response import json_success
from zerver.models import UserProfile, UserMessage, get_usermessage_by_message_id

def __tmp2(request: __typ0, __tmp0: UserProfile) :
    return json_success({'pointer': __tmp0.pointer})

@has_request_variables
def __tmp1(request: __typ0, __tmp0: <FILL>,
                           pointer: int=REQ(converter=to_non_negative_int)) -> __typ1:
    if pointer <= __tmp0.pointer:
        return json_success()

    if get_usermessage_by_message_id(__tmp0, pointer) is None:
        raise JsonableError(_("Invalid message ID"))

    request._log_data["extra"] = "[%s]" % (pointer,)
    update_flags = (request.client.name.lower() in ['android', "zulipandroid"])
    do_update_pointer(__tmp0, request.client, pointer, update_flags=update_flags)

    return json_success()
