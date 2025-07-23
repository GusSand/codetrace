from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
from django.http import HttpRequest, HttpResponse

from zerver.models import UserProfile
from zerver.lib.actions import notify_attachment_update
from zerver.lib.validator import check_int
from zerver.lib.response import json_success
from zerver.lib.attachments import user_attachments, remove_attachment, \
    access_attachment_by_id


def __tmp0(request: <FILL>, __tmp1: __typ0) :
    return json_success({"attachments": user_attachments(__tmp1)})


def remove(request, __tmp1: __typ0, attachment_id: int) -> HttpResponse:
    attachment = access_attachment_by_id(__tmp1, attachment_id,
                                         needs_owner=True)
    notify_attachment_update(__tmp1, "remove", {"id": attachment.id})
    remove_attachment(__tmp1, attachment)
    return json_success()
