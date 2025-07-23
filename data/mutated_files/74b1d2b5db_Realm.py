from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "bool"
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

def copy_user_settings(__tmp7: __typ1, __tmp1: __typ1) :
    """Warning: Does not save, to avoid extra database queries"""
    for settings_name in __typ1.property_types:
        value = getattr(__tmp7, settings_name)
        setattr(__tmp1, settings_name, value)

    for settings_name in __typ1.notification_setting_types:
        value = getattr(__tmp7, settings_name)
        setattr(__tmp1, settings_name, value)

    setattr(__tmp1, "full_name", __tmp7.full_name)
    setattr(__tmp1, "enter_sends", __tmp7.enter_sends)
    __tmp1.save()

    if __tmp7.avatar_source == __typ1.AVATAR_FROM_USER:
        from zerver.lib.actions import do_change_avatar_fields
        do_change_avatar_fields(__tmp1, __typ1.AVATAR_FROM_USER)
        copy_avatar(__tmp7, __tmp1)

    copy_hotpots(__tmp7, __tmp1)

# create_user_profile is based on Django's User.objects.create_user,
# except that we don't save to the database so it can used in
# bulk_creates
#
# Only use this for bulk_create -- for normal usage one should use
# create_user (below) which will also make the Subscription and
# Recipient objects
def __tmp0(__tmp5: Realm, __tmp2: __typ0, __tmp6: Optional[__typ0],
                        active: __typ2, bot_type, full_name: __typ0,
                        __tmp3: __typ0, __tmp8,
                        __tmp4: __typ2, tos_version: Optional[__typ0],
                        timezone: Optional[__typ0],
                        tutorial_status: Optional[__typ0] = __typ1.TUTORIAL_WAITING,
                        enter_sends: __typ2 = False) -> __typ1:
    now = timezone_now()
    __tmp2 = UserManager.normalize_email(__tmp2)

    user_profile = __typ1(__tmp2=__tmp2, is_staff=False, is_active=active,
                               full_name=full_name, __tmp3=__tmp3,
                               last_login=now, date_joined=now, __tmp5=__tmp5,
                               pointer=-1, is_bot=__typ2(bot_type), bot_type=bot_type,
                               __tmp8=__tmp8, __tmp4=__tmp4,
                               tos_version=tos_version, timezone=timezone,
                               tutorial_status=tutorial_status,
                               enter_sends=enter_sends,
                               onboarding_steps=ujson.dumps([]),
                               default_language=__tmp5.default_language,
                               twenty_four_hour_time=__tmp5.default_twenty_four_hour_time,
                               delivery_email=__tmp2)

    if bot_type or not active:
        __tmp6 = None

    user_profile.set_password(__tmp6)

    user_profile.api_key = generate_api_key()
    return user_profile

def create_user(__tmp2, __tmp6, __tmp5: <FILL>,
                full_name, __tmp3: __typ0, active: __typ2 = True,
                is_realm_admin: __typ2 = False, bot_type: Optional[int] = None,
                __tmp8: Optional[__typ1] = None,
                tos_version: Optional[__typ0] = None, timezone: __typ0 = "",
                avatar_source: __typ0 = __typ1.AVATAR_FROM_GRAVATAR,
                __tmp4: __typ2 = False,
                default_sending_stream: Optional[Stream] = None,
                default_events_register_stream: Optional[Stream] = None,
                default_all_public_streams: Optional[__typ2] = None,
                __tmp7: Optional[__typ1] = None) :
    user_profile = __tmp0(__tmp5, __tmp2, __tmp6, active, bot_type,
                                       full_name, __tmp3, __tmp8,
                                       __tmp4, tos_version, timezone)
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
    if __tmp7 is not None:
        # copy_user_settings saves the attribute values so a secondary
        # save is not required.
        copy_user_settings(__tmp7, user_profile)
    else:
        user_profile.save()

    recipient = Recipient.objects.create(type_id=user_profile.id,
                                         type=Recipient.PERSONAL)
    Subscription.objects.create(user_profile=user_profile, recipient=recipient)
    return user_profile
