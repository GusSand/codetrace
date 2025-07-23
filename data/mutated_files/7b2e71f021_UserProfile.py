from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"

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

def mute_topic(__tmp1: <FILL>, __tmp2: str,
               topic_name: str) -> __typ0:
    (stream, recipient, sub) = access_stream_by_name(__tmp1, __tmp2)

    if topic_is_muted(__tmp1, stream.id, topic_name):
        return json_error(_("Topic already muted"))

    do_mute_topic(__tmp1, stream, recipient, topic_name)
    return json_success()

def unmute_topic(__tmp1, __tmp2,
                 topic_name) :
    error = _("Topic is not muted")
    stream = access_stream_for_unmute_topic(__tmp1, __tmp2, error)

    if not topic_is_muted(__tmp1, stream.id, topic_name):
        return json_error(error)

    do_unmute_topic(__tmp1, stream, topic_name)
    return json_success()

@has_request_variables
def __tmp0(request, __tmp1, stream: str=REQ(),
                       topic: str=REQ(), op: str=REQ()) :

    if op == 'add':
        return mute_topic(__tmp1, stream, topic)
    elif op == 'remove':
        return unmute_topic(__tmp1, stream, topic)
