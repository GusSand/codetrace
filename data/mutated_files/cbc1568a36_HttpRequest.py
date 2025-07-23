from typing import TypeAlias
__typ1 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "str"

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

def mute_topic(user_profile: UserProfile, __tmp1: __typ0,
               __tmp0: __typ0) :
    (stream, recipient, sub) = access_stream_by_name(user_profile, __tmp1)

    if topic_is_muted(user_profile, stream.id, __tmp0):
        return json_error(_("Topic already muted"))

    do_mute_topic(user_profile, stream, recipient, __tmp0)
    return json_success()

def unmute_topic(user_profile, __tmp1: __typ0,
                 __tmp0) -> __typ1:
    error = _("Topic is not muted")
    stream = access_stream_for_unmute_topic(user_profile, __tmp1, error)

    if not topic_is_muted(user_profile, stream.id, __tmp0):
        return json_error(error)

    do_unmute_topic(user_profile, stream, __tmp0)
    return json_success()

@has_request_variables
def update_muted_topic(request: <FILL>, user_profile, stream: __typ0=REQ(),
                       topic: __typ0=REQ(), op: __typ0=REQ()) :

    if op == 'add':
        return mute_topic(user_profile, stream, topic)
    elif op == 'remove':
        return unmute_topic(user_profile, stream, topic)
