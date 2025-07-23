from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "Realm"

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

def __tmp9(__tmp10: <FILL>, __tmp12: str) -> List[str]:
    frags = __tmp10.split(',')
    __tmp5 = [s.strip().lower() for s in frags]
    __tmp5 = [email for email in __tmp5 if email]

    if len(__tmp5) > 1:
        __tmp5 = [email for email in __tmp5 if email != __tmp12.lower()]

    return __tmp5

def __tmp7(__tmp5: Iterable[str], realm) -> List[__typ0]:
    __tmp3 = []  # type: List[UserProfile]
    for email in __tmp5:
        try:
            __tmp6 = get_user_including_cross_realm(email, realm)
        except __typ0.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        __tmp3.append(__tmp6)
    return __tmp3

def __tmp15(__tmp5: Iterable[str], realm: __typ1) -> List[__typ0]:
    try:
        return __tmp7(__tmp5, realm)
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
    def __tmp13(__tmp2, __tmp1: str,
                 __tmp3: Optional[Sequence[__typ0]]=None,
                 __tmp11: Optional[str]=None,
                 __tmp17: Optional[str]=None) -> None:
        assert(__tmp1 in ['stream', 'private'])
        __tmp2._msg_type = __tmp1
        __tmp2._user_profiles = __tmp3
        __tmp2._stream_name = __tmp11
        __tmp2._topic = __tmp17

    def is_stream(__tmp2) -> bool:
        return __tmp2._msg_type == 'stream'

    def is_private(__tmp2) -> bool:
        return __tmp2._msg_type == 'private'

    def __tmp3(__tmp2) :
        assert(__tmp2.is_private())
        return __tmp2._user_profiles  # type: ignore # assertion protects us

    def __tmp11(__tmp2) -> str:
        assert(__tmp2.is_stream())
        assert(__tmp2._stream_name is not None)
        return __tmp2._stream_name

    def __tmp17(__tmp2) :
        assert(__tmp2.is_stream())
        assert(__tmp2._topic is not None)
        return __tmp2._topic

    @staticmethod
    def __tmp0(sender: __typ0,
                     __tmp14: str,
                     __tmp16: Sequence[str],
                     __tmp8: str,
                     realm: Optional[__typ1]=None) -> 'Addressee':

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = sender.realm

        if __tmp14 == 'stream':
            if len(__tmp16) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if __tmp16:
                __tmp11 = __tmp16[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if sender.default_sending_stream:
                    # Use the users default stream
                    __tmp11 = sender.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return Addressee.for_stream(__tmp11, __tmp8)
        elif __tmp14 == 'private':
            __tmp5 = __tmp16
            return Addressee.for_private(__tmp5, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp11: str, __tmp17: str) -> 'Addressee':
        if __tmp17 is None:
            raise JsonableError(_("Missing topic"))
        __tmp17 = __tmp17.strip()
        if __tmp17 == "":
            raise JsonableError(_("Topic can't be empty"))
        return Addressee(
            __tmp1='stream',
            __tmp11=__tmp11,
            __tmp17=__tmp17,
        )

    @staticmethod
    def for_private(__tmp5: Sequence[str], realm: __typ1) -> 'Addressee':
        __tmp3 = __tmp15(__tmp5, realm)
        return Addressee(
            __tmp1='private',
            __tmp3=__tmp3,
        )

    @staticmethod
    def __tmp4(__tmp6: __typ0) -> 'Addressee':
        __tmp3 = [__tmp6]
        return Addressee(
            __tmp1='private',
            __tmp3=__tmp3,
        )
