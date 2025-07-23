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

def raw_pm_with_emails(__tmp7: __typ0, __tmp4: __typ0) :
    frags = __tmp7.split(',')
    emails = [s.strip().lower() for s in frags]
    emails = [email for email in emails if email]

    if len(emails) > 1:
        emails = [email for email in emails if email != __tmp4.lower()]

    return emails

def __tmp3(emails: Iterable[__typ0], realm: Realm) :
    __tmp1 = []  # type: List[UserProfile]
    for email in emails:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except __typ1.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        __tmp1.append(user_profile)
    return __tmp1

def __tmp8(emails: Iterable[__typ0], realm) -> List[__typ1]:
    try:
        return __tmp3(emails, realm)
    except ValidationError as e:
        assert isinstance(e.messages[0], __typ0)
        raise JsonableError(e.messages[0])

class __typ3:
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
    def __tmp6(__tmp0, msg_type: __typ0,
                 __tmp1: Optional[Sequence[__typ1]]=None,
                 __tmp5: Optional[__typ0]=None,
                 __tmp10: Optional[__typ0]=None) -> None:
        assert(msg_type in ['stream', 'private'])
        __tmp0._msg_type = msg_type
        __tmp0._user_profiles = __tmp1
        __tmp0._stream_name = __tmp5
        __tmp0._topic = __tmp10

    def is_stream(__tmp0) :
        return __tmp0._msg_type == 'stream'

    def is_private(__tmp0) -> __typ2:
        return __tmp0._msg_type == 'private'

    def __tmp1(__tmp0) :
        assert(__tmp0.is_private())
        return __tmp0._user_profiles  # type: ignore # assertion protects us

    def __tmp5(__tmp0) :
        assert(__tmp0.is_stream())
        assert(__tmp0._stream_name is not None)
        return __tmp0._stream_name

    def __tmp10(__tmp0) -> __typ0:
        assert(__tmp0.is_stream())
        assert(__tmp0._topic is not None)
        return __tmp0._topic

    @staticmethod
    def legacy_build(__tmp2: __typ1,
                     message_type_name: __typ0,
                     __tmp9,
                     topic_name: __typ0,
                     realm: Optional[Realm]=None) -> 'Addressee':

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = __tmp2.realm

        if message_type_name == 'stream':
            if len(__tmp9) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if __tmp9:
                __tmp5 = __tmp9[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if __tmp2.default_sending_stream:
                    # Use the users default stream
                    __tmp5 = __tmp2.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return __typ3.for_stream(__tmp5, topic_name)
        elif message_type_name == 'private':
            emails = __tmp9
            return __typ3.for_private(emails, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(__tmp5: __typ0, __tmp10: __typ0) -> 'Addressee':
        if __tmp10 is None:
            raise JsonableError(_("Missing topic"))
        __tmp10 = __tmp10.strip()
        if __tmp10 == "":
            raise JsonableError(_("Topic can't be empty"))
        return __typ3(
            msg_type='stream',
            __tmp5=__tmp5,
            __tmp10=__tmp10,
        )

    @staticmethod
    def for_private(emails: Sequence[__typ0], realm: <FILL>) :
        __tmp1 = __tmp8(emails, realm)
        return __typ3(
            msg_type='private',
            __tmp1=__tmp1,
        )

    @staticmethod
    def for_user_profile(user_profile) -> 'Addressee':
        __tmp1 = [user_profile]
        return __typ3(
            msg_type='private',
            __tmp1=__tmp1,
        )
