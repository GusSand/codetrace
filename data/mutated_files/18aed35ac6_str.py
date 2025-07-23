from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "Realm"

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

def raw_pm_with_emails(__tmp6: str, my_email: str) -> List[str]:
    frags = __tmp6.split(',')
    __tmp3 = [s.strip().lower() for s in frags]
    __tmp3 = [email for email in __tmp3 if email]

    if len(__tmp3) > 1:
        __tmp3 = [email for email in __tmp3 if email != my_email.lower()]

    return __tmp3

def __tmp5(__tmp3: Iterable[str], realm: __typ2) -> List[__typ1]:
    user_profiles = []  # type: List[UserProfile]
    for email in __tmp3:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except __typ1.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        user_profiles.append(user_profile)
    return user_profiles

def get_user_profiles(__tmp3: Iterable[str], realm: __typ2) -> List[__typ1]:
    try:
        return __tmp5(__tmp3, realm)
    except ValidationError as e:
        assert isinstance(e.messages[0], str)
        raise JsonableError(e.messages[0])

class __typ0:
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
    def __init__(__tmp1, __tmp0: str,
                 user_profiles: Optional[Sequence[__typ1]]=None,
                 __tmp7: Optional[str]=None,
                 topic: Optional[str]=None) -> None:
        assert(__tmp0 in ['stream', 'private'])
        __tmp1._msg_type = __tmp0
        __tmp1._user_profiles = user_profiles
        __tmp1._stream_name = __tmp7
        __tmp1._topic = topic

    def is_stream(__tmp1) -> bool:
        return __tmp1._msg_type == 'stream'

    def is_private(__tmp1) :
        return __tmp1._msg_type == 'private'

    def user_profiles(__tmp1) -> List[__typ1]:
        assert(__tmp1.is_private())
        return __tmp1._user_profiles  # type: ignore # assertion protects us

    def __tmp7(__tmp1) -> str:
        assert(__tmp1.is_stream())
        assert(__tmp1._stream_name is not None)
        return __tmp1._stream_name

    def topic(__tmp1) :
        assert(__tmp1.is_stream())
        assert(__tmp1._topic is not None)
        return __tmp1._topic

    @staticmethod
    def legacy_build(__tmp4: __typ1,
                     message_type_name: <FILL>,
                     __tmp8: Sequence[str],
                     topic_name: str,
                     realm: Optional[__typ2]=None) -> 'Addressee':

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = __tmp4.realm

        if message_type_name == 'stream':
            if len(__tmp8) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if __tmp8:
                __tmp7 = __tmp8[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if __tmp4.default_sending_stream:
                    # Use the users default stream
                    __tmp7 = __tmp4.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return __typ0.for_stream(__tmp7, topic_name)
        elif message_type_name == 'private':
            __tmp3 = __tmp8
            return __typ0.for_private(__tmp3, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp7: str, topic: str) -> 'Addressee':
        if topic is None:
            raise JsonableError(_("Missing topic"))
        topic = topic.strip()
        if topic == "":
            raise JsonableError(_("Topic can't be empty"))
        return __typ0(
            __tmp0='stream',
            __tmp7=__tmp7,
            topic=topic,
        )

    @staticmethod
    def for_private(__tmp3: Sequence[str], realm: __typ2) -> 'Addressee':
        user_profiles = get_user_profiles(__tmp3, realm)
        return __typ0(
            __tmp0='private',
            user_profiles=user_profiles,
        )

    @staticmethod
    def __tmp2(user_profile: __typ1) -> 'Addressee':
        user_profiles = [user_profile]
        return __typ0(
            __tmp0='private',
            user_profiles=user_profiles,
        )
