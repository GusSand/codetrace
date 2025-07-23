from typing import TypeAlias
__typ2 : TypeAlias = "Realm"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
import urllib
from typing import Any, Dict, List

from zerver.lib.topic import get_topic_from_message_info
from zerver.models import Realm, Stream, UserProfile

def __tmp0(__tmp14: __typ1) -> __typ1:
    # Do the same encoding operation as hash_util.encodeHashComponent on the
    # frontend.
    # `safe` has a default value of "/", but we want those encoded, too.
    return urllib.parse.quote(
        __tmp14.encode("utf-8"), safe=b"").replace(".", "%2E").replace("%", ".")

def __tmp4(__tmp8: __typ0, __tmp12) -> __typ1:
    # We encode streams for urls as something like 99-Verona.
    __tmp12 = __tmp12.replace(' ', '-')
    return __typ1(__tmp8) + '-' + __tmp0(__tmp12)

def __tmp2(__tmp9: __typ2, __tmp6: UserProfile) :
    base_url = "%s/#narrow/pm-with/" % (__tmp9.uri,)
    email_user = __tmp6.email.split('@')[0].lower()
    pm_slug = __typ1(__tmp6.id) + '-' + __tmp0(email_user)
    return base_url + pm_slug

def __tmp3(__tmp9, __tmp13) -> __typ1:
    pm_slug = ','.join(__typ1(user_id) for user_id in sorted(__tmp13)) + '-group'
    base_url = "%s/#narrow/pm-with/" % (__tmp9.uri,)
    return base_url + pm_slug

def __tmp15(__tmp9: __typ2, __tmp11: <FILL>) :
    base_url = "%s/#narrow/stream/" % (__tmp9.uri,)
    return base_url + __tmp4(__tmp11.id, __tmp11.name)

def __tmp10(__tmp9: __typ2, __tmp11, topic) -> __typ1:
    base_url = "%s/#narrow/stream/" % (__tmp9.uri,)
    return "%s%s/topic/%s" % (base_url,
                              __tmp4(__tmp11.id, __tmp11.name),
                              __tmp0(topic))

def __tmp1(__tmp9,
                     message) -> __typ1:

    if message['type'] == 'stream':
        url = __tmp5(
            __tmp9=__tmp9,
            message=message,
        )
        return url

    url = __tmp7(
        __tmp9=__tmp9,
        message=message,
    )
    return url

def __tmp5(__tmp9: __typ2,
                            message) -> __typ1:
    message_id = __typ1(message['id'])
    __tmp8 = message['stream_id']
    __tmp12 = message['display_recipient']
    topic_name = get_topic_from_message_info(message)
    encoded_topic = __tmp0(topic_name)
    encoded_stream = __tmp4(__tmp8=__tmp8, __tmp12=__tmp12)

    parts = [
        __tmp9.uri,
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

def __tmp7(__tmp9: __typ2,
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
        __tmp9.uri,
        '#narrow',
        'pm-with',
        pm_str,
        'near',
        message_id,
    ]
    full_url = '/'.join(parts)
    return full_url
