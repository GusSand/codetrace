from typing import TypeAlias
__typ2 : TypeAlias = "Stream"
__typ1 : TypeAlias = "Realm"
__typ0 : TypeAlias = "str"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def hash_util_encode(__tmp6) :
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        __tmp6.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def encode_stream(stream_id: <FILL>, stream_name: __typ0) -> __typ0:
    # We encode streams for urls as something like 99-Verona.
    stream_name = stream_name.replace(' ', '-')
    return __typ0(stream_id) + '-' + hash_util_encode(stream_name)

def personal_narrow_url(__tmp3, __tmp2) :
    base_url = "%s/#narrow/pm-with/" % (__tmp3.uri,)
    email_user = __tmp2.email.split('@')[0].lower()
    pm_slug = __typ0(__tmp2.id) + '-' + hash_util_encode(email_user)
    return base_url + pm_slug

def __tmp0(__tmp3: __typ1, __tmp5: List[int]) -> __typ0:
    pm_slug = ','.join(__typ0(user_id) for user_id in sorted(__tmp5)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp3.uri,)
    return base_url + pm_slug

def stream_narrow_url(__tmp3, stream) :
    base_url = "%s/#narrow/stream/" % (__tmp3.uri,)
    return base_url + encode_stream(stream.id, stream.name)

def __tmp4(__tmp3: __typ1, stream, topic: __typ0) -> __typ0:
    base_url = "%s/#narrow/stream/" % (__tmp3.uri,)
    return "%s%s/topic/%s" % (base_url,
                              encode_stream(stream.id, stream.name),
                              hash_util_encode(topic))

def near_message_url(__tmp3,
                     message: Dict[__typ0, Any]) :

    if message['type'] == 'stream':
        url = near_stream_message_url(
            __tmp3=__tmp3,
            message=message,
        )
        return url

    url = __tmp1(
        __tmp3=__tmp3,
        message=message,
    )
    return url

def near_stream_message_url(__tmp3: __typ1,
                            message: Dict[__typ0, Any]) :
    message_id = __typ0(message['id'])
    stream_id = message['stream_id']
    stream_name = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = hash_util_encode(topic_name)
    encoded_stream = encode_stream(stream_id=stream_id, stream_name=stream_name)

    parts = [
        __tmp3.uri,
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

def __tmp1(__tmp3: __typ1,
                        message) :
    message_id = __typ0(message['id'])
    str_user_ids = [
        __typ0(recipient['id'])
        for recipient in message['display_recipient']
    ]

    # Use the "perma-link" format here that includes the sender's
    # user_id, so they're easier to share between people.
    pm_str = ','.join(str_user_ids) + '-pm'

    parts = [
        __tmp3.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
