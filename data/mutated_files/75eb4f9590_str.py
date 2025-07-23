from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "Realm"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def hash_util_encode(string: str) -> str:
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        string.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def encode_stream(stream_id: int, stream_name: <FILL>) -> str:
    # We encode streams for urls as something like 99-Verona.
    stream_name = stream_name.replace(' ', '-')
    return str(stream_id) + '-' + hash_util_encode(stream_name)

def personal_narrow_url(__tmp3, sender) -> str:
    base_url = "%s/#narrow/pm-with/" % (__tmp3.uri,)
    email_user = sender.email.split('@')[0].lower()
    pm_slug = str(sender.id) + '-' + hash_util_encode(email_user)
    return base_url + pm_slug

def __tmp1(__tmp3: __typ1, other_user_ids) -> str:
    pm_slug = ','.join(str(user_id) for user_id in sorted(other_user_ids)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp3.uri,)
    return base_url + pm_slug

def __tmp6(__tmp3, __tmp5) -> str:
    base_url = "%s/#narrow/stream/" % (__tmp3.uri,)
    return base_url + encode_stream(__tmp5.id, __tmp5.name)

def __tmp4(__tmp3: __typ1, __tmp5, topic: str) :
    base_url = "%s/#narrow/stream/" % (__tmp3.uri,)
    return "%s%s/topic/%s" % (base_url,
                              encode_stream(__tmp5.id, __tmp5.name),
                              hash_util_encode(topic))

def __tmp0(__tmp3: __typ1,
                     message: Dict[str, Any]) -> str:

    if message['type'] == 'stream':
        url = __tmp2(
            __tmp3=__tmp3,
            message=message,
        )
        return url

    url = near_pm_message_url(
        __tmp3=__tmp3,
        message=message,
    )
    return url

def __tmp2(__tmp3: __typ1,
                            message: Dict[str, Any]) -> str:
    message_id = str(message['id'])
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

def near_pm_message_url(__tmp3,
                        message: Dict[str, Any]) -> str:
    message_id = str(message['id'])
    str_user_ids = [
        str(recipient['id'])
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
