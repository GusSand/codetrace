from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "Attachment"

from django.utils.translation import ugettext as _
from typing import Any, Dict, List

from zerver.lib.request import JsonableError
from zerver.lib.upload import delete_message_image
from zerver.models import Attachment, UserProfile

def __tmp4(__tmp1: __typ1) -> List[Dict[str, Any]]:
    attachments = __typ0.objects.filter(owner=__tmp1).prefetch_related('messages')
    return [a.to_dict() for a in attachments]

def access_attachment_by_id(__tmp1: __typ1, __tmp0: <FILL>,
                            needs_owner: bool=False) -> __typ0:
    query = __typ0.objects.filter(id=__tmp0)
    if needs_owner:
        query = query.filter(owner=__tmp1)

    __tmp2 = query.first()
    if __tmp2 is None:
        raise JsonableError(_("Invalid attachment"))
    return __tmp2

def __tmp3(__tmp1: __typ1, __tmp2: __typ0) -> None:
    try:
        delete_message_image(__tmp2.path_id)
    except Exception:
        raise JsonableError(_("An error occurred while deleting the attachment. Please try again later."))
    __tmp2.delete()
