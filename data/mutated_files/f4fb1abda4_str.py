from typing import TypeAlias
__typ1 : TypeAlias = "bool"

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

def raw_pm_with_emails(email_str: str, __tmp8: <FILL>) :
    frags = email_str.split(',')
    __tmp3 = [s.strip().lower() for s in frags]
    __tmp3 = [email for email in __tmp3 if email]

    if len(__tmp3) > 1:
        __tmp3 = [email for email in __tmp3 if email != __tmp8.lower()]

    return __tmp3

def __tmp4(__tmp3, realm) :
    __tmp1 = []  # type: List[UserProfile]
    for email in __tmp3:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except UserProfile.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        __tmp1.append(user_profile)
    return __tmp1

def get_user_profiles(__tmp3, realm) :
    try:
        return __tmp4(__tmp3, realm)
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
    def __tmp6(__tmp2, __tmp0,
                 __tmp1: Optional[Sequence[UserProfile]]=None,
                 __tmp7: Optional[str]=None,
                 topic: Optional[str]=None) :
        assert(__tmp0 in ['stream', 'private'])
        __tmp2._msg_type = __tmp0
        __tmp2._user_profiles = __tmp1
        __tmp2._stream_name = __tmp7
        __tmp2._topic = topic

    def is_stream(__tmp2) :
        return __tmp2._msg_type == 'stream'

    def is_private(__tmp2) :
        return __tmp2._msg_type == 'private'

    def __tmp1(__tmp2) -> List[UserProfile]:
        assert(__tmp2.is_private())
        return __tmp2._user_profiles  # type: ignore # assertion protects us

    def __tmp7(__tmp2) :
        assert(__tmp2.is_stream())
        assert(__tmp2._stream_name is not None)
        return __tmp2._stream_name

    def topic(__tmp2) :
        assert(__tmp2.is_stream())
        assert(__tmp2._topic is not None)
        return __tmp2._topic

    @staticmethod
    def legacy_build(sender,
                     message_type_name,
                     message_to,
                     __tmp5,
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
                __tmp7 = message_to[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if sender.default_sending_stream:
                    # Use the users default stream
                    __tmp7 = sender.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return __typ0.for_stream(__tmp7, __tmp5)
        elif message_type_name == 'private':
            __tmp3 = message_to
            return __typ0.for_private(__tmp3, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp7, topic) :
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
    def for_private(__tmp3, realm: Realm) :
        __tmp1 = get_user_profiles(__tmp3, realm)
        return __typ0(
            __tmp0='private',
            __tmp1=__tmp1,
        )

    @staticmethod
    def for_user_profile(user_profile) -> 'Addressee':
        __tmp1 = [user_profile]
        return __typ0(
            __tmp0='private',
            __tmp1=__tmp1,
        )
