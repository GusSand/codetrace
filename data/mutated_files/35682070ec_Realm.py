from typing import TypeAlias
__typ0 : TypeAlias = "str"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def __tmp0(__tmp11: __typ0) -> __typ0:
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        __tmp11.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def __tmp2(stream_id: int, __tmp9: __typ0) -> __typ0:
    # We encode streams for urls as something like 99-Verona.
    __tmp9 = __tmp9.replace(' ', '-')
    return __typ0(stream_id) + '-' + __tmp0(__tmp9)

def personal_narrow_url(__tmp6: Realm, __tmp4: UserProfile) -> __typ0:
    base_url = "%s/#narrow/pm-with/" % (__tmp6.uri,)
    email_user = __tmp4.email.split('@')[0].lower()
    pm_slug = __typ0(__tmp4.id) + '-' + __tmp0(email_user)
    return base_url + pm_slug

def huddle_narrow_url(__tmp6, __tmp10: List[int]) -> __typ0:
    pm_slug = ','.join(__typ0(user_id) for user_id in sorted(__tmp10)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp6.uri,)
    return base_url + pm_slug

def __tmp12(__tmp6: <FILL>, __tmp8: Stream) -> __typ0:
    base_url = "%s/#narrow/stream/" % (__tmp6.uri,)
    return base_url + __tmp2(__tmp8.id, __tmp8.name)

def __tmp7(__tmp6: Realm, __tmp8: Stream, topic: __typ0) -> __typ0:
    base_url = "%s/#narrow/stream/" % (__tmp6.uri,)
    return "%s%s/topic/%s" % (base_url,
                              __tmp2(__tmp8.id, __tmp8.name),
                              __tmp0(topic))

def __tmp1(__tmp6: Realm,
                     message) -> __typ0:

    if message['type'] == 'stream':
        url = __tmp3(
            __tmp6=__tmp6,
            message=message,
        )
        return url

    url = __tmp5(
        __tmp6=__tmp6,
        message=message,
    )
    return url

def __tmp3(__tmp6,
                            message: Dict[__typ0, Any]) -> __typ0:
    message_id = __typ0(message['id'])
    stream_id = message['stream_id']
    __tmp9 = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = __tmp0(topic_name)
    encoded_stream = __tmp2(stream_id=stream_id, __tmp9=__tmp9)

    parts = [
        __tmp6.uri,
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

def __tmp5(__tmp6: Realm,
                        message: Dict[__typ0, Any]) -> __typ0:
    message_id = __typ0(message['id'])
    str_user_ids = [
        __typ0(recipient['id'])
        for recipient in message['display_recipient']
    ]

    # Use the "perma-link" format here that includes the sender's
    # user_id, so they're easier to share between people.
    pm_str = ','.join(str_user_ids) + '-pm'

    parts = [
        __tmp6.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
