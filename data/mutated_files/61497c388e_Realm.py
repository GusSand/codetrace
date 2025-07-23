from typing import TypeAlias
__typ3 : TypeAlias = "Stream"
__typ2 : TypeAlias = "UserProfile"
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

def encode_stream(stream_id: __typ0, stream_name) :
    # We encode streams for urls as something like 99-Verona.
    stream_name = stream_name.replace(' ', '-')
    return __typ1(stream_id) + '-' + hash_util_encode(stream_name)

def personal_narrow_url(realm: <FILL>, sender: __typ2) :
    base_url = "%s/#narrow/pm-with/" % (realm.uri,)
    email_user = sender.email.split('@')[0].lower()
    pm_slug = __typ1(sender.id) + '-' + hash_util_encode(email_user)
    return base_url + pm_slug

def huddle_narrow_url(realm, other_user_ids) :
    pm_slug = ','.join(__typ1(user_id) for user_id in sorted(other_user_ids)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (realm.uri,)
    return base_url + pm_slug

def stream_narrow_url(realm, stream: __typ3) :
    base_url = "%s/#narrow/stream/" % (realm.uri,)
    return base_url + encode_stream(stream.id, stream.name)

def __tmp0(realm, stream: __typ3, topic: __typ1) -> __typ1:
    base_url = "%s/#narrow/stream/" % (realm.uri,)
    return "%s%s/topic/%s" % (base_url,
                              encode_stream(stream.id, stream.name),
                              hash_util_encode(topic))

def __tmp1(realm,
                     message: Dict[__typ1, Any]) -> __typ1:

    if message['type'] == 'stream':
        url = near_stream_message_url(
            realm=realm,
            message=message,
        )
        return url

    url = __tmp2(
        realm=realm,
        message=message,
    )
    return url

def near_stream_message_url(realm,
                            message) :
    message_id = __typ1(message['id'])
    stream_id = message['stream_id']
    stream_name = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = hash_util_encode(topic_name)
    encoded_stream = encode_stream(stream_id=stream_id, stream_name=stream_name)

    parts = [
        realm.uri,
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

def __tmp2(realm: Realm,
                        message) :
    message_id = __typ1(message['id'])
    str_user_ids = [
        __typ1(recipient['id'])
        for recipient in message['display_recipient']
    ]

    # Use the "perma-link" format here that includes the sender's
    # user_id, so they're easier to share between people.
    pm_str = ','.join(str_user_ids) + '-pm'

    parts = [
        realm.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
