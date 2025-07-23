from typing import TypeAlias
__typ1 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "int"
from django.http import HttpRequest, HttpResponse

from zerver.models import UserProfile
from zerver.lib.actions import notify_attachment_update
from zerver.lib.validator import check_int
from zerver.lib.response import json_success
from zerver.lib.attachments import user_attachments, remove_attachment, \
    access_attachment_by_id


def list_by_user(__tmp0, user_profile: <FILL>) :
    return json_success({"attachments": user_attachments(user_profile)})


def remove(__tmp0, user_profile, __tmp1) :
    attachment = access_attachment_by_id(user_profile, __tmp1,
                                         needs_owner=True)
    notify_attachment_update(user_profile, "remove", {"id": attachment.id})
    remove_attachment(user_profile, attachment)
    return json_success()
