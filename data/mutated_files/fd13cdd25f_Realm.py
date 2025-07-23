from typing import TypeAlias
__typ2 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"

from typing import Iterable, List, Optional, Sequence

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.lib.request import JsonableError
from zerver.models import (
    Realm,
    UserProfile,
    get_user_including_cross_realm,
)

def __tmp4(email_str, my_email) :
    frags = email_str.split(',')
    __tmp1 = [s.strip().lower() for s in frags]
    __tmp1 = [email for email in __tmp1 if email]

    if len(__tmp1) > 1:
        __tmp1 = [email for email in __tmp1 if email != my_email.lower()]

    return __tmp1

def __tmp2(__tmp1, realm: <FILL>) :
    user_profiles = []  # type: List[UserProfile]
    for email in __tmp1:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except __typ2.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        user_profiles.append(user_profile)
    return user_profiles

def __tmp7(__tmp1, realm) :
    try:
        return __tmp2(__tmp1, realm)
    except ValidationError as e:
        assert isinstance(e.messages[0], __typ0)
        raise JsonableError(e.messages[0])

class __typ1:
    # This is really just a holder for vars that tended to be passed
    # around in a non-type-safe way before this class was introduced.
    #
    # It also avoids some nonsense where you have to think about whether
    # topic should be None or '' for a PM, or you have to make an array
    # of one stream.
    #
    # Eventually we can use this to cache Stream and UserProfile objects
    # in memory.
    #
    # This should be treated as an immutable class.
    def __init__(__tmp0, msg_type,
                 user_profiles: Optional[Sequence[__typ2]]=None,
                 __tmp5: Optional[__typ0]=None,
                 topic: Optional[__typ0]=None) :
        assert(msg_type in ['stream', 'private'])
        __tmp0._msg_type = msg_type
        __tmp0._user_profiles = user_profiles
        __tmp0._stream_name = __tmp5
        __tmp0._topic = topic

    def is_stream(__tmp0) :
        return __tmp0._msg_type == 'stream'

    def is_private(__tmp0) :
        return __tmp0._msg_type == 'private'

    def user_profiles(__tmp0) :
        assert(__tmp0.is_private())
        return __tmp0._user_profiles  # type: ignore # assertion protects us

    def __tmp5(__tmp0) :
        assert(__tmp0.is_stream())
        assert(__tmp0._stream_name is not None)
        return __tmp0._stream_name

    def topic(__tmp0) :
        assert(__tmp0.is_stream())
        assert(__tmp0._topic is not None)
        return __tmp0._topic

    @staticmethod
    def __tmp6(sender,
                     message_type_name,
                     message_to,
                     __tmp3,
                     realm: Optional[Realm]=None) :

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = sender.realm

        if message_type_name == 'stream':
            if len(message_to) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if message_to:
                __tmp5 = message_to[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if sender.default_sending_stream:
                    # Use the users default stream
                    __tmp5 = sender.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return __typ1.for_stream(__tmp5, __tmp3)
        elif message_type_name == 'private':
            __tmp1 = message_to
            return __typ1.for_private(__tmp1, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp5, topic) :
        if topic is None:
            raise JsonableError(_("Missing topic"))
        topic = topic.strip()
        if topic == "":
            raise JsonableError(_("Topic can't be empty"))
        return __typ1(
            msg_type='stream',
            __tmp5=__tmp5,
            topic=topic,
        )

    @staticmethod
    def for_private(__tmp1, realm) :
        user_profiles = __tmp7(__tmp1, realm)
        return __typ1(
            msg_type='private',
            user_profiles=user_profiles,
        )

    @staticmethod
    def for_user_profile(user_profile) :
        user_profiles = [user_profile]
        return __typ1(
            msg_type='private',
            user_profiles=user_profiles,
        )
