from typing import TypeAlias
__typ3 : TypeAlias = "Stream"
__typ2 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def hash_util_encode(string: __typ1) -> __typ1:
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        string.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def encode_stream(stream_id: __typ0, stream_name: __typ1) -> __typ1:
    # We encode streams for urls as something like 99-Verona.
    stream_name = stream_name.replace(' ', '-')
    return __typ1(stream_id) + '-' + hash_util_encode(stream_name)

def personal_narrow_url(__tmp0: Realm, sender: __typ2) -> __typ1:
    base_url = "%s/#narrow/pm-with/" % (__tmp0.uri,)
    email_user = sender.email.split('@')[0].lower()
    pm_slug = __typ1(sender.id) + '-' + hash_util_encode(email_user)
    return base_url + pm_slug

def huddle_narrow_url(__tmp0: Realm, other_user_ids: List[__typ0]) -> __typ1:
    pm_slug = ','.join(__typ1(user_id) for user_id in sorted(other_user_ids)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp0.uri,)
    return base_url + pm_slug

def stream_narrow_url(__tmp0: Realm, stream: __typ3) :
    base_url = "%s/#narrow/stream/" % (__tmp0.uri,)
    return base_url + encode_stream(stream.id, stream.name)

def topic_narrow_url(__tmp0: Realm, stream: __typ3, topic: __typ1) -> __typ1:
    base_url = "%s/#narrow/stream/" % (__tmp0.uri,)
    return "%s%s/topic/%s" % (base_url,
                              encode_stream(stream.id, stream.name),
                              hash_util_encode(topic))

def near_message_url(__tmp0: <FILL>,
                     message: Dict[__typ1, Any]) -> __typ1:

    if message['type'] == 'stream':
        url = near_stream_message_url(
            __tmp0=__tmp0,
            message=message,
        )
        return url

    url = near_pm_message_url(
        __tmp0=__tmp0,
        message=message,
    )
    return url

def near_stream_message_url(__tmp0,
                            message: Dict[__typ1, Any]) -> __typ1:
    message_id = __typ1(message['id'])
    stream_id = message['stream_id']
    stream_name = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = hash_util_encode(topic_name)
    encoded_stream = encode_stream(stream_id=stream_id, stream_name=stream_name)

    parts = [
        __tmp0.uri,
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

def near_pm_message_url(__tmp0: Realm,
                        message: Dict[__typ1, Any]) -> __typ1:
    message_id = __typ1(message['id'])
    str_user_ids = [
        __typ1(recipient['id'])
        for recipient in message['display_recipient']
    ]

    # Use the "perma-link" format here that includes the sender's
    # user_id, so they're easier to share between people.
    pm_str = ','.join(str_user_ids) + '-pm'

    parts = [
        __tmp0.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
