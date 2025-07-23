from typing import TypeAlias
__typ2 : TypeAlias = "HttpResponse"
__typ1 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "str"

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Callable

from confirmation.models import Confirmation, get_object_from_key, \
    render_confirmation_key_error, ConfirmationKeyException
from zerver.lib.actions import do_change_notification_settings, clear_scheduled_emails
from zerver.models import UserProfile, ScheduledEmail
from zerver.context_processors import common_context

def process_unsubscribe(__tmp5: __typ1, confirmation_key: __typ0, __tmp0,
                        __tmp4) -> __typ2:
    try:
        __tmp2 = get_object_from_key(confirmation_key, Confirmation.UNSUBSCRIBE)
    except ConfirmationKeyException:
        return render(__tmp5, 'zerver/unsubscribe_link_error.html')

    __tmp4(__tmp2)
    context = common_context(__tmp2)
    context.update({"subscription_type": __tmp0})
    return render(__tmp5, 'zerver/unsubscribe_success.html', context=context)

# Email unsubscribe functions. All have the function signature
# processor(user_profile).

def __tmp7(__tmp2: UserProfile) :
    do_change_notification_settings(__tmp2, 'enable_offline_email_notifications', False)

def __tmp1(__tmp2) :
    clear_scheduled_emails(__tmp2.id, ScheduledEmail.WELCOME)

def __tmp9(__tmp2: <FILL>) :
    do_change_notification_settings(__tmp2, 'enable_digest_emails', False)

def __tmp8(__tmp2: UserProfile) :
    do_change_notification_settings(__tmp2, 'enable_login_emails', False)

# The keys are part of the URL for the unsubscribe link and must be valid
# without encoding.
# The values are a tuple of (display name, unsubscribe function), where the
# display name is what we call this class of email in user-visible text.
email_unsubscribers = {
    "missed_messages": ("missed messages", __tmp7),
    "welcome": ("welcome", __tmp1),
    "digest": ("digest", __tmp9),
    "login": ("login", __tmp8)
}

# Login NOT required. These are for one-click unsubscribes.
def __tmp3(__tmp5: __typ1, __tmp6: __typ0,
                      confirmation_key) -> __typ2:
    if __tmp6 in email_unsubscribers:
        display_name, __tmp4 = email_unsubscribers[__tmp6]
        return process_unsubscribe(__tmp5, confirmation_key, display_name, __tmp4)

    return render(__tmp5, 'zerver/unsubscribe_link_error.html')
