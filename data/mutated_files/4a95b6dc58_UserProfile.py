from typing import TypeAlias
__typ2 : TypeAlias = "Realm"
__typ0 : TypeAlias = "str"
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

def __tmp7(__tmp10, __tmp8) :
    frags = __tmp10.split(',')
    __tmp2 = [s.strip().lower() for s in frags]
    __tmp2 = [email for email in __tmp2 if email]

    if len(__tmp2) > 1:
        __tmp2 = [email for email in __tmp2 if email != __tmp8.lower()]

    return __tmp2

def __tmp5(__tmp2, realm) :
    user_profiles = []  # type: List[UserProfile]
    for email in __tmp2:
        try:
            __tmp3 = get_user_including_cross_realm(email, realm)
        except UserProfile.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        user_profiles.append(__tmp3)
    return user_profiles

def __tmp12(__tmp2, realm) :
    try:
        return __tmp5(__tmp2, realm)
    except ValidationError as e:
        assert isinstance(e.messages[0], __typ0)
        raise JsonableError(e.messages[0])

class Addressee:
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
                 user_profiles: Optional[Sequence[UserProfile]]=None,
                 __tmp9: Optional[__typ0]=None,
                 __tmp13: Optional[__typ0]=None) :
        assert(msg_type in ['stream', 'private'])
        __tmp0._msg_type = msg_type
        __tmp0._user_profiles = user_profiles
        __tmp0._stream_name = __tmp9
        __tmp0._topic = __tmp13

    def is_stream(__tmp0) :
        return __tmp0._msg_type == 'stream'

    def is_private(__tmp0) :
        return __tmp0._msg_type == 'private'

    def user_profiles(__tmp0) :
        assert(__tmp0.is_private())
        return __tmp0._user_profiles  # type: ignore # assertion protects us

    def __tmp9(__tmp0) :
        assert(__tmp0.is_stream())
        assert(__tmp0._stream_name is not None)
        return __tmp0._stream_name

    def __tmp13(__tmp0) :
        assert(__tmp0.is_stream())
        assert(__tmp0._topic is not None)
        return __tmp0._topic

    @staticmethod
    def __tmp11(__tmp4,
                     message_type_name,
                     message_to,
                     __tmp6,
                     realm: Optional[__typ2]=None) :

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = __tmp4.realm

        if message_type_name == 'stream':
            if len(message_to) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if message_to:
                __tmp9 = message_to[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if __tmp4.default_sending_stream:
                    # Use the users default stream
                    __tmp9 = __tmp4.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return Addressee.for_stream(__tmp9, __tmp6)
        elif message_type_name == 'private':
            __tmp2 = message_to
            return Addressee.for_private(__tmp2, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp9, __tmp13) :
        if __tmp13 is None:
            raise JsonableError(_("Missing topic"))
        __tmp13 = __tmp13.strip()
        if __tmp13 == "":
            raise JsonableError(_("Topic can't be empty"))
        return Addressee(
            msg_type='stream',
            __tmp9=__tmp9,
            __tmp13=__tmp13,
        )

    @staticmethod
    def for_private(__tmp2, realm) -> 'Addressee':
        user_profiles = __tmp12(__tmp2, realm)
        return Addressee(
            msg_type='private',
            user_profiles=user_profiles,
        )

    @staticmethod
    def __tmp1(__tmp3: <FILL>) :
        user_profiles = [__tmp3]
        return Addressee(
            msg_type='private',
            user_profiles=user_profiles,
        )
