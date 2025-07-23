from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"

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

def raw_pm_with_emails(email_str, my_email) :
    frags = email_str.split(',')
    __tmp4 = [s.strip().lower() for s in frags]
    __tmp4 = [email for email in __tmp4 if email]

    if len(__tmp4) > 1:
        __tmp4 = [email for email in __tmp4 if email != my_email.lower()]

    return __tmp4

def user_profiles_from_unvalidated_emails(__tmp4: Iterable[str], realm) :
    __tmp2 = []  # type: List[UserProfile]
    for email in __tmp4:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except __typ0.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        __tmp2.append(user_profile)
    return __tmp2

def __tmp7(__tmp4, realm) :
    try:
        return user_profiles_from_unvalidated_emails(__tmp4, realm)
    except ValidationError as e:
        assert isinstance(e.messages[0], str)
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
    def __init__(__tmp1, __tmp0: <FILL>,
                 __tmp2: Optional[Sequence[__typ0]]=None,
                 __tmp6: Optional[str]=None,
                 __tmp8: Optional[str]=None) :
        assert(__tmp0 in ['stream', 'private'])
        __tmp1._msg_type = __tmp0
        __tmp1._user_profiles = __tmp2
        __tmp1._stream_name = __tmp6
        __tmp1._topic = __tmp8

    def is_stream(__tmp1) :
        return __tmp1._msg_type == 'stream'

    def is_private(__tmp1) :
        return __tmp1._msg_type == 'private'

    def __tmp2(__tmp1) :
        assert(__tmp1.is_private())
        return __tmp1._user_profiles  # type: ignore # assertion protects us

    def __tmp6(__tmp1) :
        assert(__tmp1.is_stream())
        assert(__tmp1._stream_name is not None)
        return __tmp1._stream_name

    def __tmp8(__tmp1) :
        assert(__tmp1.is_stream())
        assert(__tmp1._topic is not None)
        return __tmp1._topic

    @staticmethod
    def legacy_build(sender,
                     __tmp3,
                     message_to,
                     __tmp5,
                     realm: Optional[Realm]=None) :

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = sender.realm

        if __tmp3 == 'stream':
            if len(message_to) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if message_to:
                __tmp6 = message_to[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if sender.default_sending_stream:
                    # Use the users default stream
                    __tmp6 = sender.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return Addressee.for_stream(__tmp6, __tmp5)
        elif __tmp3 == 'private':
            __tmp4 = message_to
            return Addressee.for_private(__tmp4, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp6, __tmp8) :
        if __tmp8 is None:
            raise JsonableError(_("Missing topic"))
        __tmp8 = __tmp8.strip()
        if __tmp8 == "":
            raise JsonableError(_("Topic can't be empty"))
        return Addressee(
            __tmp0='stream',
            __tmp6=__tmp6,
            __tmp8=__tmp8,
        )

    @staticmethod
    def for_private(__tmp4, realm) :
        __tmp2 = __tmp7(__tmp4, realm)
        return Addressee(
            __tmp0='private',
            __tmp2=__tmp2,
        )

    @staticmethod
    def for_user_profile(user_profile) :
        __tmp2 = [user_profile]
        return Addressee(
            __tmp0='private',
            __tmp2=__tmp2,
        )
