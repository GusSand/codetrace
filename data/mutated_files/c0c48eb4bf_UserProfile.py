from typing import TypeAlias
__typ0 : TypeAlias = "Attachment"
__typ1 : TypeAlias = "int"

from django.utils.translation import ugettext as _
from typing import Any, Dict, List

from zerver.lib.request import JsonableError
from zerver.lib.upload import delete_message_image
from zerver.models import Attachment, UserProfile

def user_attachments(user_profile) -> List[Dict[str, Any]]:
    attachments = __typ0.objects.filter(owner=user_profile).prefetch_related('messages')
    return [a.to_dict() for a in attachments]

def __tmp0(user_profile: <FILL>, attachment_id: __typ1,
                            needs_owner: bool=False) :
    query = __typ0.objects.filter(id=attachment_id)
    if needs_owner:
        query = query.filter(owner=user_profile)

    attachment = query.first()
    if attachment is None:
        raise JsonableError(_("Invalid attachment"))
    return attachment

def remove_attachment(user_profile, attachment: __typ0) :
    try:
        delete_message_image(attachment.path_id)
    except Exception:
        raise JsonableError(_("An error occurred while deleting the attachment. Please try again later."))
    attachment.delete()
