from typing import TypeAlias
__typ2 : TypeAlias = "Realm"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def hash_util_encode(string) :
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        string.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def __tmp3(__tmp4: __typ0, __tmp9) :
    # We encode streams for urls as something like 99-Verona.
    __tmp9 = __tmp9.replace(' ', '-')
    return __typ1(__tmp4) + '-' + hash_util_encode(__tmp9)

def __tmp1(__tmp7, __tmp5: <FILL>) :
    base_url = "%s/#narrow/pm-with/" % (__tmp7.uri,)
    email_user = __tmp5.email.split('@')[0].lower()
    pm_slug = __typ1(__tmp5.id) + '-' + hash_util_encode(email_user)
    return base_url + pm_slug

def __tmp2(__tmp7, __tmp10) :
    pm_slug = ','.join(__typ1(user_id) for user_id in sorted(__tmp10)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp7.uri,)
    return base_url + pm_slug

def stream_narrow_url(__tmp7, stream) :
    base_url = "%s/#narrow/stream/" % (__tmp7.uri,)
    return base_url + __tmp3(stream.id, stream.name)

def __tmp8(__tmp7, stream, topic) :
    base_url = "%s/#narrow/stream/" % (__tmp7.uri,)
    return "%s%s/topic/%s" % (base_url,
                              __tmp3(stream.id, stream.name),
                              hash_util_encode(topic))

def __tmp0(__tmp7,
                     message: Dict[__typ1, Any]) :

    if message['type'] == 'stream':
        url = near_stream_message_url(
            __tmp7=__tmp7,
            message=message,
        )
        return url

    url = __tmp6(
        __tmp7=__tmp7,
        message=message,
    )
    return url

def near_stream_message_url(__tmp7,
                            message) -> __typ1:
    message_id = __typ1(message['id'])
    __tmp4 = message['stream_id']
    __tmp9 = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = hash_util_encode(topic_name)
    encoded_stream = __tmp3(__tmp4=__tmp4, __tmp9=__tmp9)

    parts = [
        __tmp7.uri,
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

def __tmp6(__tmp7,
                        message: Dict[__typ1, Any]) :
    message_id = __typ1(message['id'])
    str_user_ids = [
        __typ1(recipient['id'])
        for recipient in message['display_recipient']
    ]

    # Use the "perma-link" format here that includes the sender's
    # user_id, so they're easier to share between people.
    pm_str = ','.join(str_user_ids) + '-pm'

    parts = [
        __tmp7.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
