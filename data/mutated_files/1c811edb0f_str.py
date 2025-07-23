from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "Realm"

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

def raw_pm_with_emails(email_str: str, my_email: str) -> List[str]:
    frags = email_str.split(',')
    emails = [s.strip().lower() for s in frags]
    emails = [email for email in emails if email]

    if len(emails) > 1:
        emails = [email for email in emails if email != my_email.lower()]

    return emails

def user_profiles_from_unvalidated_emails(emails: Iterable[str], realm: __typ3) -> List[__typ1]:
    user_profiles = []  # type: List[UserProfile]
    for email in emails:
        try:
            user_profile = get_user_including_cross_realm(email, realm)
        except __typ1.DoesNotExist:
            raise ValidationError(_("Invalid email '%s'") % (email,))
        user_profiles.append(user_profile)
    return user_profiles

def get_user_profiles(emails: Iterable[str], realm: __typ3) -> List[__typ1]:
    try:
        return user_profiles_from_unvalidated_emails(emails, realm)
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
    def __init__(__tmp0, msg_type: str,
                 user_profiles: Optional[Sequence[__typ1]]=None,
                 stream_name: Optional[str]=None,
                 topic: Optional[str]=None) :
        assert(msg_type in ['stream', 'private'])
        __tmp0._msg_type = msg_type
        __tmp0._user_profiles = user_profiles
        __tmp0._stream_name = stream_name
        __tmp0._topic = topic

    def is_stream(__tmp0) :
        return __tmp0._msg_type == 'stream'

    def is_private(__tmp0) -> __typ2:
        return __tmp0._msg_type == 'private'

    def user_profiles(__tmp0) -> List[__typ1]:
        assert(__tmp0.is_private())
        return __tmp0._user_profiles  # type: ignore # assertion protects us

    def stream_name(__tmp0) -> str:
        assert(__tmp0.is_stream())
        assert(__tmp0._stream_name is not None)
        return __tmp0._stream_name

    def topic(__tmp0) -> str:
        assert(__tmp0.is_stream())
        assert(__tmp0._topic is not None)
        return __tmp0._topic

    @staticmethod
    def legacy_build(sender,
                     message_type_name: str,
                     message_to: Sequence[str],
                     topic_name,
                     realm: Optional[__typ3]=None) -> 'Addressee':

        # For legacy reason message_to used to be either a list of
        # emails or a list of streams.  We haven't fixed all of our
        # callers yet.
        if realm is None:
            realm = sender.realm

        if message_type_name == 'stream':
            if len(message_to) > 1:
                raise JsonableError(_("Cannot send to multiple streams"))

            if message_to:
                stream_name = message_to[0]
            else:
                # This is a hack to deal with the fact that we still support
                # default streams (and the None will be converted later in the
                # callpath).
                if sender.default_sending_stream:
                    # Use the users default stream
                    stream_name = sender.default_sending_stream.name
                else:
                    raise JsonableError(_('Missing stream'))

            return __typ0.for_stream(stream_name, topic_name)
        elif message_type_name == 'private':
            emails = message_to
            return __typ0.for_private(emails, realm)
        else:
            raise JsonableError(_("Invalid message type"))

    @staticmethod
    def for_stream(stream_name: <FILL>, topic) -> 'Addressee':
        if topic is None:
            raise JsonableError(_("Missing topic"))
        topic = topic.strip()
        if topic == "":
            raise JsonableError(_("Topic can't be empty"))
        return __typ0(
            msg_type='stream',
            stream_name=stream_name,
            topic=topic,
        )

    @staticmethod
    def for_private(emails: Sequence[str], realm: __typ3) -> 'Addressee':
        user_profiles = get_user_profiles(emails, realm)
        return __typ0(
            msg_type='private',
            user_profiles=user_profiles,
        )

    @staticmethod
    def for_user_profile(user_profile: __typ1) -> 'Addressee':
        user_profiles = [user_profile]
        return __typ0(
            msg_type='private',
            user_profiles=user_profiles,
        )
