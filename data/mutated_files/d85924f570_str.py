from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "Realm"
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

def copy_user_settings(source_profile: __typ0, target_profile) -> None:
    """Warning: Does not save, to avoid extra database queries"""
    for settings_name in __typ0.property_types:
        value = getattr(source_profile, settings_name)
        setattr(target_profile, settings_name, value)

    for settings_name in __typ0.notification_setting_types:
        value = getattr(source_profile, settings_name)
        setattr(target_profile, settings_name, value)

    setattr(target_profile, "full_name", source_profile.full_name)
    setattr(target_profile, "enter_sends", source_profile.enter_sends)
    target_profile.save()

    if source_profile.avatar_source == __typ0.AVATAR_FROM_USER:
        from zerver.lib.actions import do_change_avatar_fields
        do_change_avatar_fields(target_profile, __typ0.AVATAR_FROM_USER)
        copy_avatar(source_profile, target_profile)

    copy_hotpots(source_profile, target_profile)

# create_user_profile is based on Django's User.objects.create_user,
# except that we don't save to the database so it can used in
# bulk_creates
#
# Only use this for bulk_create -- for normal usage one should use
# create_user (below) which will also make the Subscription and
# Recipient objects
def create_user_profile(realm: __typ2, email, password: Optional[str],
                        __tmp0: __typ1, bot_type, full_name: <FILL>,
                        short_name, bot_owner,
                        is_mirror_dummy, tos_version: Optional[str],
                        timezone,
                        tutorial_status: Optional[str] = __typ0.TUTORIAL_WAITING,
                        enter_sends: __typ1 = False) -> __typ0:
    now = timezone_now()
    email = UserManager.normalize_email(email)

    user_profile = __typ0(email=email, is_staff=False, is_active=__tmp0,
                               full_name=full_name, short_name=short_name,
                               last_login=now, date_joined=now, realm=realm,
                               pointer=-1, is_bot=__typ1(bot_type), bot_type=bot_type,
                               bot_owner=bot_owner, is_mirror_dummy=is_mirror_dummy,
                               tos_version=tos_version, timezone=timezone,
                               tutorial_status=tutorial_status,
                               enter_sends=enter_sends,
                               onboarding_steps=ujson.dumps([]),
                               default_language=realm.default_language,
                               twenty_four_hour_time=realm.default_twenty_four_hour_time,
                               delivery_email=email)

    if bot_type or not __tmp0:
        password = None

    user_profile.set_password(password)

    user_profile.api_key = generate_api_key()
    return user_profile

def create_user(email, password: Optional[str], realm,
                full_name: str, short_name, __tmp0: __typ1 = True,
                is_realm_admin: __typ1 = False, bot_type: Optional[int] = None,
                bot_owner: Optional[__typ0] = None,
                tos_version: Optional[str] = None, timezone: str = "",
                avatar_source: str = __typ0.AVATAR_FROM_GRAVATAR,
                is_mirror_dummy: __typ1 = False,
                default_sending_stream: Optional[Stream] = None,
                default_events_register_stream: Optional[Stream] = None,
                default_all_public_streams: Optional[__typ1] = None,
                source_profile: Optional[__typ0] = None) -> __typ0:
    user_profile = create_user_profile(realm, email, password, __tmp0, bot_type,
                                       full_name, short_name, bot_owner,
                                       is_mirror_dummy, tos_version, timezone)
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
        copy_user_settings(source_profile, user_profile)
    else:
        user_profile.save()

    recipient = Recipient.objects.create(type_id=user_profile.id,
                                         type=Recipient.PERSONAL)
    Subscription.objects.create(user_profile=user_profile, recipient=recipient)
    return user_profile
