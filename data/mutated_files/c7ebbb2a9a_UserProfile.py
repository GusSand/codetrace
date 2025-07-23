from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"

from django.contrib.auth.models import UserManager
from django.utils.timezone import now as timezone_now
from zerver.models import UserProfile, Recipient, Subscription, Realm, Stream
from zerver.lib.upload import copy_avatar
from zerver.lib.hotspots import copy_hotpots
from zerver.lib.utils import generate_api_key

import base64
import ujson
import os
import string

from typing import Optional

def __tmp1(source_profile, __tmp8: <FILL>) -> None:
    """Warning: Does not save, to avoid extra database queries"""
    for settings_name in UserProfile.property_types:
        value = getattr(source_profile, settings_name)
        setattr(__tmp8, settings_name, value)

    for settings_name in UserProfile.notification_setting_types:
        value = getattr(source_profile, settings_name)
        setattr(__tmp8, settings_name, value)

    setattr(__tmp8, "full_name", source_profile.full_name)
    setattr(__tmp8, "enter_sends", source_profile.enter_sends)
    __tmp8.save()

    if source_profile.avatar_source == UserProfile.AVATAR_FROM_USER:
        from zerver.lib.actions import do_change_avatar_fields
        do_change_avatar_fields(__tmp8, UserProfile.AVATAR_FROM_USER)
        copy_avatar(source_profile, __tmp8)

    copy_hotpots(source_profile, __tmp8)

# create_user_profile is based on Django's User.objects.create_user,
# except that we don't save to the database so it can used in
# bulk_creates
#
# Only use this for bulk_create -- for normal usage one should use
# create_user (below) which will also make the Subscription and
# Recipient objects
def __tmp0(__tmp6: Realm, __tmp2: __typ0, __tmp7,
                        __tmp11: __typ1, bot_type, full_name: __typ0,
                        __tmp3: __typ0, __tmp10: Optional[UserProfile],
                        __tmp4: __typ1, __tmp9,
                        timezone: Optional[__typ0],
                        tutorial_status: Optional[__typ0] = UserProfile.TUTORIAL_WAITING,
                        enter_sends: __typ1 = False) :
    now = timezone_now()
    __tmp2 = UserManager.normalize_email(__tmp2)

    user_profile = UserProfile(__tmp2=__tmp2, is_staff=False, is_active=__tmp11,
                               full_name=full_name, __tmp3=__tmp3,
                               last_login=now, date_joined=now, __tmp6=__tmp6,
                               pointer=-1, is_bot=__typ1(bot_type), bot_type=bot_type,
                               __tmp10=__tmp10, __tmp4=__tmp4,
                               __tmp9=__tmp9, timezone=timezone,
                               tutorial_status=tutorial_status,
                               enter_sends=enter_sends,
                               onboarding_steps=ujson.dumps([]),
                               default_language=__tmp6.default_language,
                               twenty_four_hour_time=__tmp6.default_twenty_four_hour_time,
                               delivery_email=__tmp2)

    if bot_type or not __tmp11:
        __tmp7 = None

    user_profile.set_password(__tmp7)

    user_profile.api_key = generate_api_key()
    return user_profile

def __tmp5(__tmp2: __typ0, __tmp7, __tmp6: Realm,
                full_name: __typ0, __tmp3: __typ0, __tmp11: __typ1 = True,
                is_realm_admin: __typ1 = False, bot_type: Optional[int] = None,
                __tmp10: Optional[UserProfile] = None,
                __tmp9: Optional[__typ0] = None, timezone: __typ0 = "",
                avatar_source: __typ0 = UserProfile.AVATAR_FROM_GRAVATAR,
                __tmp4: __typ1 = False,
                default_sending_stream: Optional[Stream] = None,
                default_events_register_stream: Optional[Stream] = None,
                default_all_public_streams: Optional[__typ1] = None,
                source_profile: Optional[UserProfile] = None) -> UserProfile:
    user_profile = __tmp0(__tmp6, __tmp2, __tmp7, __tmp11, bot_type,
                                       full_name, __tmp3, __tmp10,
                                       __tmp4, __tmp9, timezone)
    user_profile.is_realm_admin = is_realm_admin
    user_profile.avatar_source = avatar_source
    user_profile.timezone = timezone
    user_profile.default_sending_stream = default_sending_stream
    user_profile.default_events_register_stream = default_events_register_stream
    # Allow the ORM default to be used if not provided
    if default_all_public_streams is not None:
        user_profile.default_all_public_streams = default_all_public_streams
    # If a source profile was specified, we copy settings from that
    # user.  Note that this is positioned in a way that overrides
    # other arguments passed in, which is correct for most defaults
    # like timezone where the source profile likely has a better value
    # than the guess. As we decide on details like avatars and full
    # names for this feature, we may want to move it.
    if source_profile is not None:
        # copy_user_settings saves the attribute values so a secondary
        # save is not required.
        __tmp1(source_profile, user_profile)
    else:
        user_profile.save()

    recipient = Recipient.objects.create(type_id=user_profile.id,
                                         type=Recipient.PERSONAL)
    Subscription.objects.create(user_profile=user_profile, recipient=recipient)
    return user_profile
