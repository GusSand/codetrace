from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "HttpRequest"

from django.http import HttpResponse, HttpRequest
from typing import List

import ujson

from django.utils.translation import ugettext as _
from zerver.lib.actions import do_mute_topic, do_unmute_topic
from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success, json_error
from zerver.lib.topic_mutes import topic_is_muted
from zerver.lib.streams import access_stream_by_name, access_stream_for_unmute_topic
from zerver.lib.validator import check_string, check_list
from zerver.models import get_stream, Stream, UserProfile

def mute_topic(__tmp1, __tmp3,
               __tmp0: <FILL>) -> __typ2:
    (stream, recipient, sub) = access_stream_by_name(__tmp1, __tmp3)

    if topic_is_muted(__tmp1, stream.id, __tmp0):
        return json_error(_("Topic already muted"))

    do_mute_topic(__tmp1, stream, recipient, __tmp0)
    return json_success()

def unmute_topic(__tmp1, __tmp3,
                 __tmp0) :
    error = _("Topic is not muted")
    stream = access_stream_for_unmute_topic(__tmp1, __tmp3, error)

    if not topic_is_muted(__tmp1, stream.id, __tmp0):
        return json_error(error)

    do_unmute_topic(__tmp1, stream, __tmp0)
    return json_success()

@has_request_variables
def __tmp2(request: __typ0, __tmp1, stream: str=REQ(),
                       topic: str=REQ(), op: str=REQ()) -> __typ2:

    if op == 'add':
        return mute_topic(__tmp1, stream, topic)
    elif op == 'remove':
        return unmute_topic(__tmp1, stream, topic)
