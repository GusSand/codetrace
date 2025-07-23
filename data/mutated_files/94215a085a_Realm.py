from typing import TypeAlias
__typ2 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def __tmp0(string) :
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        string.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def __tmp2(stream_id, stream_name) :
    # We encode streams for urls as something like 99-Verona.
    stream_name = stream_name.replace(' ', '-')
    return __typ0(stream_id) + '-' + __tmp0(stream_name)

def __tmp1(__tmp4, __tmp3) :
    base_url = "%s/#narrow/pm-with/" % (__tmp4.uri,)
    email_user = __tmp3.email.split('@')[0].lower()
    pm_slug = __typ0(__tmp3.id) + '-' + __tmp0(email_user)
    return base_url + pm_slug

def huddle_narrow_url(__tmp4, other_user_ids) :
    pm_slug = ','.join(__typ0(user_id) for user_id in sorted(other_user_ids)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp4.uri,)
    return base_url + pm_slug

def stream_narrow_url(__tmp4, __tmp5) -> __typ0:
    base_url = "%s/#narrow/stream/" % (__tmp4.uri,)
    return base_url + __tmp2(__tmp5.id, __tmp5.name)

def topic_narrow_url(__tmp4: Realm, __tmp5, topic) :
    base_url = "%s/#narrow/stream/" % (__tmp4.uri,)
    return "%s%s/topic/%s" % (base_url,
                              __tmp2(__tmp5.id, __tmp5.name),
                              __tmp0(topic))

def near_message_url(__tmp4,
                     message) :

    if message['type'] == 'stream':
        url = __tmp6(
            __tmp4=__tmp4,
            message=message,
        )
        return url

    url = near_pm_message_url(
        __tmp4=__tmp4,
        message=message,
    )
    return url

def __tmp6(__tmp4: Realm,
                            message) :
    message_id = __typ0(message['id'])
    stream_id = message['stream_id']
    stream_name = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = __tmp0(topic_name)
    encoded_stream = __tmp2(stream_id=stream_id, stream_name=stream_name)

    parts = [
        __tmp4.uri,
        '#narrow',
        'stream',
        encoded_stream,
        'topic',
        encoded_topic,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url

def near_pm_message_url(__tmp4: <FILL>,
                        message) -> __typ0:
    message_id = __typ0(message['id'])
    str_user_ids = [
        __typ0(recipient['id'])
        for recipient in message['display_recipient']
    ]

    # Use the "perma-link" format here that includes the sender's
    # user_id, so they're easier to share between people.
    pm_str = ','.join(str_user_ids) + '-pm'

    parts = [
        __tmp4.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
