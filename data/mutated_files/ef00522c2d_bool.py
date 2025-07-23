from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "str"

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

def __tmp0(__tmp9: __typ1, __tmp10) :
    """Warning: Does not save, to avoid extra database queries"""
    for settings_name in __typ1.property_types:
        value = getattr(__tmp9, settings_name)
        setattr(__tmp10, settings_name, value)

    for settings_name in __typ1.notification_setting_types:
        value = getattr(__tmp9, settings_name)
        setattr(__tmp10, settings_name, value)

    setattr(__tmp10, "full_name", __tmp9.full_name)
    setattr(__tmp10, "enter_sends", __tmp9.enter_sends)
    __tmp10.save()

    if __tmp9.avatar_source == __typ1.AVATAR_FROM_USER:
        from zerver.lib.actions import do_change_avatar_fields
        do_change_avatar_fields(__tmp10, __typ1.AVATAR_FROM_USER)
        copy_avatar(__tmp9, __tmp10)

    copy_hotpots(__tmp9, __tmp10)

# create_user_profile is based on Django's User.objects.create_user,
# except that we don't save to the database so it can used in
# bulk_creates
#
# Only use this for bulk_create -- for normal usage one should use
# create_user (below) which will also make the Subscription and
# Recipient objects
def __tmp1(__tmp7: Realm, __tmp3, __tmp8: Optional[__typ0],
                        __tmp12: <FILL>, __tmp2, full_name: __typ0,
                        __tmp4, __tmp11,
                        __tmp5: bool, tos_version,
                        timezone,
                        tutorial_status: Optional[__typ0] = __typ1.TUTORIAL_WAITING,
                        enter_sends: bool = False) -> __typ1:
    now = timezone_now()
    __tmp3 = UserManager.normalize_email(__tmp3)

    user_profile = __typ1(__tmp3=__tmp3, is_staff=False, is_active=__tmp12,
                               full_name=full_name, __tmp4=__tmp4,
                               last_login=now, date_joined=now, __tmp7=__tmp7,
                               pointer=-1, is_bot=bool(__tmp2), __tmp2=__tmp2,
                               __tmp11=__tmp11, __tmp5=__tmp5,
                               tos_version=tos_version, timezone=timezone,
                               tutorial_status=tutorial_status,
                               enter_sends=enter_sends,
                               onboarding_steps=ujson.dumps([]),
                               default_language=__tmp7.default_language,
                               twenty_four_hour_time=__tmp7.default_twenty_four_hour_time,
                               delivery_email=__tmp3)

    if __tmp2 or not __tmp12:
        __tmp8 = None

    user_profile.set_password(__tmp8)

    user_profile.api_key = generate_api_key()
    return user_profile

def __tmp6(__tmp3: __typ0, __tmp8: Optional[__typ0], __tmp7: Realm,
                full_name: __typ0, __tmp4, __tmp12: bool = True,
                is_realm_admin: bool = False, __tmp2: Optional[int] = None,
                __tmp11: Optional[__typ1] = None,
                tos_version: Optional[__typ0] = None, timezone: __typ0 = "",
                avatar_source: __typ0 = __typ1.AVATAR_FROM_GRAVATAR,
                __tmp5: bool = False,
                default_sending_stream: Optional[Stream] = None,
                default_events_register_stream: Optional[Stream] = None,
                default_all_public_streams: Optional[bool] = None,
                __tmp9: Optional[__typ1] = None) :
    user_profile = __tmp1(__tmp7, __tmp3, __tmp8, __tmp12, __tmp2,
                                       full_name, __tmp4, __tmp11,
                                       __tmp5, tos_version, timezone)
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
    if __tmp9 is not None:
        # copy_user_settings saves the attribute values so a secondary
        # save is not required.
        __tmp0(__tmp9, user_profile)
    else:
        user_profile.save()

    recipient = Recipient.objects.create(type_id=user_profile.id,
                                         type=Recipient.PERSONAL)
    Subscription.objects.create(user_profile=user_profile, recipient=recipient)
    return user_profile
