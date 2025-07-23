from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ2 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "HttpResponse"
from django.http import HttpRequest, HttpResponse

from zerver.models import UserProfile
from zerver.lib.actions import notify_attachment_update
from zerver.lib.validator import check_int
from zerver.lib.response import json_success
from zerver.lib.attachments import user_attachments, remove_attachment, \
    access_attachment_by_id


def __tmp0(__tmp2, __tmp1) :
    return json_success({"attachments": user_attachments(__tmp1)})


def remove(__tmp2, __tmp1, attachment_id: <FILL>) :
    attachment = access_attachment_by_id(__tmp1, attachment_id,
                                         needs_owner=True)
    notify_attachment_update(__tmp1, "remove", {"id": attachment.id})
    remove_attachment(__tmp1, attachment)
    return json_success()
