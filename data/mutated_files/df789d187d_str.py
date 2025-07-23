from typing import TypeAlias
__typ2 : TypeAlias = "Realm"
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

def raw_pm_with_emails(__tmp8, __tmp6) -> List[str]:
    frags = __tmp8.split(',')
    __tmp3 = [s.strip().lower() for s in frags]
    __tmp3 = [email for email in __tmp3 if email]

    if len(__tmp3) > 1:
        __tmp3 = [email for email in __tmp3 if email != __tmp6.lower()]

    return __tmp3

def user_profiles_from_unvalidated_emails(__tmp3: Iterable[str], realm) :
    __tmp0 = []  # type: List[UserProfile]
    for email in __tmp3:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except UserProfile.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        __tmp0.append(user_profile)
    return __tmp0

def __tmp11(__tmp3, realm: __typ2) :
    try:
        return user_profiles_from_unvalidated_emails(__tmp3, realm)
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
    def __tmp9(__tmp1, msg_type,
                 __tmp0: Optional[Sequence[UserProfile]]=None,
                 __tmp7: Optional[str]=None,
                 __tmp13: Optional[str]=None) :
        assert(msg_type in ['stream', 'private'])
        __tmp1._msg_type = msg_type
        __tmp1._user_profiles = __tmp0
        __tmp1._stream_name = __tmp7
        __tmp1._topic = __tmp13

    def is_stream(__tmp1) :
        return __tmp1._msg_type == 'stream'

    def is_private(__tmp1) :
        return __tmp1._msg_type == 'private'

    def __tmp0(__tmp1) :
        assert(__tmp1.is_private())
        return __tmp1._user_profiles  # type: ignore # assertion protects us

    def __tmp7(__tmp1) :
        assert(__tmp1.is_stream())
        assert(__tmp1._stream_name is not None)
        return __tmp1._stream_name

    def __tmp13(__tmp1) -> str:
        assert(__tmp1.is_stream())
        assert(__tmp1._topic is not None)
        return __tmp1._topic

    @staticmethod
    def legacy_build(__tmp4: UserProfile,
                     __tmp10,
                     __tmp12,
                     __tmp5,
                     realm: Optional[__typ2]=None) :

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = __tmp4.realm

        if __tmp10 == 'stream':
            if len(__tmp12) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if __tmp12:
                __tmp7 = __tmp12[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if __tmp4.default_sending_stream:
                    # Use the users default stream
                    __tmp7 = __tmp4.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return __typ0.for_stream(__tmp7, __tmp5)
        elif __tmp10 == 'private':
            __tmp3 = __tmp12
            return __typ0.for_private(__tmp3, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp7, __tmp13: <FILL>) -> 'Addressee':
        if __tmp13 is None:
            raise JsonableError(_("Missing topic"))
        __tmp13 = __tmp13.strip()
        if __tmp13 == "":
            raise JsonableError(_("Topic can't be empty"))
        return __typ0(
            msg_type='stream',
            __tmp7=__tmp7,
            __tmp13=__tmp13,
        )

    @staticmethod
    def for_private(__tmp3, realm) :
        __tmp0 = __tmp11(__tmp3, realm)
        return __typ0(
            msg_type='private',
            __tmp0=__tmp0,
        )

    @staticmethod
    def __tmp2(user_profile) -> 'Addressee':
        __tmp0 = [user_profile]
        return __typ0(
            msg_type='private',
            __tmp0=__tmp0,
        )
