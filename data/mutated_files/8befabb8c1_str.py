from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "HttpRequest"

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Callable

from confirmation.models import Confirmation, get_object_from_key, \
    render_confirmation_key_error, ConfirmationKeyException
from zerver.lib.actions import do_change_notification_settings, clear_scheduled_emails
from zerver.models import UserProfile, ScheduledEmail
from zerver.context_processors import common_context

def __tmp0(__tmp3, confirmation_key: <FILL>, subscription_type: str,
                        __tmp4) :
    try:
        __tmp1 = get_object_from_key(confirmation_key, Confirmation.UNSUBSCRIBE)
    except ConfirmationKeyException:
        return render(__tmp3, 'zerver/unsubscribe_link_error.html')

    __tmp4(__tmp1)
    context = common_context(__tmp1)
    context.update({"subscription_type": subscription_type})
    return render(__tmp3, 'zerver/unsubscribe_success.html', context=context)

# Email unsubscribe functions. All have the function signature
# processor(user_profile).

def do_missedmessage_unsubscribe(__tmp1) -> None:
    do_change_notification_settings(__tmp1, 'enable_offline_email_notifications', False)

def do_welcome_unsubscribe(__tmp1) :
    clear_scheduled_emails(__tmp1.id, ScheduledEmail.WELCOME)

def do_digest_unsubscribe(__tmp1: __typ1) -> None:
    do_change_notification_settings(__tmp1, 'enable_digest_emails', False)

def do_login_unsubscribe(__tmp1) :
    do_change_notification_settings(__tmp1, 'enable_login_emails', False)

# The keys are part of the URL for the unsubscribe link and must be valid
# without encoding.
# The values are a tuple of (display name, unsubscribe function), where the
# display name is what we call this class of email in user-visible text.
email_unsubscribers = {
    "missed_messages": ("missed messages", do_missedmessage_unsubscribe),
    "welcome": ("welcome", do_welcome_unsubscribe),
    "digest": ("digest", do_digest_unsubscribe),
    "login": ("login", do_login_unsubscribe)
}

# Login NOT required. These are for one-click unsubscribes.
def email_unsubscribe(__tmp3, __tmp2,
                      confirmation_key: str) :
    if __tmp2 in email_unsubscribers:
        display_name, __tmp4 = email_unsubscribers[__tmp2]
        return __tmp0(__tmp3, confirmation_key, display_name, __tmp4)

    return render(__tmp3, 'zerver/unsubscribe_link_error.html')
