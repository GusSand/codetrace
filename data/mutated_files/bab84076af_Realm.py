from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"

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

def __tmp11(__tmp14: __typ0, __tmp4: __typ0) :
    frags = __tmp14.split(',')
    __tmp1 = [s.strip().lower() for s in frags]
    __tmp1 = [email for email in __tmp1 if email]

    if len(__tmp1) > 1:
        __tmp1 = [email for email in __tmp1 if email != __tmp4.lower()]

    return __tmp1

def __tmp10(__tmp1: Iterable[__typ0], realm: Realm) :
    __tmp9 = []  # type: List[UserProfile]
    for email in __tmp1:
        try:
            __tmp2 = get_user_including_cross_realm(email, realm)
        except __typ1.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        __tmp9.append(__tmp2)
    return __tmp9

def __tmp5(__tmp1: Iterable[__typ0], realm: <FILL>) :
    try:
        return __tmp10(__tmp1, realm)
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
    def __tmp12(__tmp0, __tmp17: __typ0,
                 __tmp9: Optional[Sequence[__typ1]]=None,
                 __tmp13: Optional[__typ0]=None,
                 __tmp16: Optional[__typ0]=None) :
        assert(__tmp17 in ['stream', 'private'])
        __tmp0._msg_type = __tmp17
        __tmp0._user_profiles = __tmp9
        __tmp0._stream_name = __tmp13
        __tmp0._topic = __tmp16

    def is_stream(__tmp0) -> __typ2:
        return __tmp0._msg_type == 'stream'

    def is_private(__tmp0) -> __typ2:
        return __tmp0._msg_type == 'private'

    def __tmp9(__tmp0) -> List[__typ1]:
        assert(__tmp0.is_private())
        return __tmp0._user_profiles  # type: ignore # assertion protects us

    def __tmp13(__tmp0) -> __typ0:
        assert(__tmp0.is_stream())
        assert(__tmp0._stream_name is not None)
        return __tmp0._stream_name

    def __tmp16(__tmp0) -> __typ0:
        assert(__tmp0.is_stream())
        assert(__tmp0._topic is not None)
        return __tmp0._topic

    @staticmethod
    def __tmp7(__tmp18: __typ1,
                     __tmp8: __typ0,
                     __tmp15: Sequence[__typ0],
                     __tmp3: __typ0,
                     realm: Optional[Realm]=None) -> 'Addressee':

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = __tmp18.realm

        if __tmp8 == 'stream':
            if len(__tmp15) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if __tmp15:
                __tmp13 = __tmp15[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if __tmp18.default_sending_stream:
                    # Use the users default stream
                    __tmp13 = __tmp18.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return Addressee.for_stream(__tmp13, __tmp3)
        elif __tmp8 == 'private':
            __tmp1 = __tmp15
            return Addressee.for_private(__tmp1, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp13: __typ0, __tmp16) :
        if __tmp16 is None:
            raise JsonableError(_("Missing topic"))
        __tmp16 = __tmp16.strip()
        if __tmp16 == "":
            raise JsonableError(_("Topic can't be empty"))
        return Addressee(
            __tmp17='stream',
            __tmp13=__tmp13,
            __tmp16=__tmp16,
        )

    @staticmethod
    def for_private(__tmp1: Sequence[__typ0], realm: Realm) -> 'Addressee':
        __tmp9 = __tmp5(__tmp1, realm)
        return Addressee(
            __tmp17='private',
            __tmp9=__tmp9,
        )

    @staticmethod
    def __tmp6(__tmp2: __typ1) -> 'Addressee':
        __tmp9 = [__tmp2]
        return Addressee(
            __tmp17='private',
            __tmp9=__tmp9,
        )
