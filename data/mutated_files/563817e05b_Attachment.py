
from django.utils.translation import ugettext as _
from typing import Any, Dict, List

from zerver.lib.request import JsonableError
from zerver.lib.upload import delete_message_image
from zerver.models import Attachment, UserProfile

def __tmp4(__tmp1) :
    attachments = Attachment.objects.filter(owner=__tmp1).prefetch_related('messages')
    return [a.to_dict() for a in attachments]

def __tmp0(__tmp1, attachment_id,
                            needs_owner: bool=False) :
    query = Attachment.objects.filter(id=attachment_id)
    if needs_owner:
        query = query.filter(owner=__tmp1)

    __tmp2 = query.first()
    if __tmp2 is None:
        raise JsonableError(_("Invalid attachment"))
    return __tmp2

def __tmp3(__tmp1, __tmp2: <FILL>) :
    try:
        delete_message_image(__tmp2.path_id)
    except Exception:
        raise JsonableError(_("An error occurred while deleting the attachment. Please try again later."))
    __tmp2.delete()
