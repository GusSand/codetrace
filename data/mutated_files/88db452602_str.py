
from django.utils.translation import ugettext as _

from zerver.lib.exceptions import ErrorCode, JsonableError

class BadEventQueueIdError(JsonableError):
    code = ErrorCode.BAD_EVENT_QUEUE_ID
    data_fields = ['queue_id']

    def __tmp2(__tmp1, queue_id: <FILL>) :
        __tmp1.queue_id = queue_id  # type: str

    @staticmethod
    def __tmp0() :
        return _("Bad event queue id: {queue_id}")
