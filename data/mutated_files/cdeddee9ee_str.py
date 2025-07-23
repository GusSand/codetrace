from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "Stream"
__typ3 : TypeAlias = "Realm"
__typ0 : TypeAlias = "int"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def hash_util_encode(string) -> str:
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        string.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def encode_stream(__tmp3: __typ0, __tmp6: str) -> str:
    # We encode streams for urls as something like 99-Verona.
    __tmp6 = __tmp6.replace(' ', '-')
    return str(__tmp3) + '-' + hash_util_encode(__tmp6)

def __tmp1(__tmp4: __typ3, __tmp2: __typ1) :
    base_url = "%s/#narrow/pm-with/" % (__tmp4.uri,)
    email_user = __tmp2.email.split('@')[0].lower()
    pm_slug = str(__tmp2.id) + '-' + hash_util_encode(email_user)
    return base_url + pm_slug

def huddle_narrow_url(__tmp4: __typ3, other_user_ids: List[__typ0]) -> str:
    pm_slug = ','.join(str(user_id) for user_id in sorted(other_user_ids)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp4.uri,)
    return base_url + pm_slug

def __tmp7(__tmp4, __tmp5: __typ2) -> str:
    base_url = "%s/#narrow/stream/" % (__tmp4.uri,)
    return base_url + encode_stream(__tmp5.id, __tmp5.name)

def topic_narrow_url(__tmp4, __tmp5: __typ2, topic: <FILL>) :
    base_url = "%s/#narrow/stream/" % (__tmp4.uri,)
    return "%s%s/topic/%s" % (base_url,
                              encode_stream(__tmp5.id, __tmp5.name),
                              hash_util_encode(topic))

def __tmp0(__tmp4: __typ3,
                     message: Dict[str, Any]) -> str:

    if message['type'] == 'stream':
        url = near_stream_message_url(
            __tmp4=__tmp4,
            message=message,
        )
        return url

    url = near_pm_message_url(
        __tmp4=__tmp4,
        message=message,
    )
    return url

def near_stream_message_url(__tmp4: __typ3,
                            message) -> str:
    message_id = str(message['id'])
    __tmp3 = message['stream_id']
    __tmp6 = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = hash_util_encode(topic_name)
    encoded_stream = encode_stream(__tmp3=__tmp3, __tmp6=__tmp6)

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

def near_pm_message_url(__tmp4,
                        message) -> str:
    message_id = str(message['id'])
    str_user_ids = [
        str(recipient['id'])
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
