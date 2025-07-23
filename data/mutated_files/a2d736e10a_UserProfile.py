
from django.utils.translation import ugettext as _
from typing import Any, Dict, List

from zerver.lib.request import JsonableError
from zerver.lib.upload import delete_message_image
from zerver.models import Attachment, UserProfile

def user_attachments(user_profile: <FILL>) -> List[Dict[str, Any]]:
    attachments = Attachment.objects.filter(owner=user_profile).prefetch_related('messages')
    return [a.to_dict() for a in attachments]

def access_attachment_by_id(user_profile: UserProfile, __tmp1: int,
                            needs_owner: bool=False) -> Attachment:
    query = Attachment.objects.filter(id=__tmp1)
    if needs_owner:
        query = query.filter(owner=user_profile)

    __tmp0 = query.first()
    if __tmp0 is None:
        raise JsonableError(_("Invalid attachment"))
    return __tmp0

def remove_attachment(user_profile, __tmp0: Attachment) :
    try:
        delete_message_image(__tmp0.path_id)
    except Exception:
        raise JsonableError(_("An error occurred while deleting the attachment. Please try again later."))
    __tmp0.delete()
