from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
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

def __tmp0(__tmp1, confirmation_key: str, subscription_type,
                        unsubscribe_function: Callable[[__typ1], None]) -> __typ2:
    try:
        __tmp2 = get_object_from_key(confirmation_key, Confirmation.UNSUBSCRIBE)
    except ConfirmationKeyException:
        return render(__tmp1, 'zerver/unsubscribe_link_error.html')

    unsubscribe_function(__tmp2)
    context = common_context(__tmp2)
    context.update({"subscription_type": subscription_type})
    return render(__tmp1, 'zerver/unsubscribe_success.html', context=context)

# Email unsubscribe functions. All have the function signature
# processor(user_profile).

def do_missedmessage_unsubscribe(__tmp2: __typ1) -> None:
    do_change_notification_settings(__tmp2, 'enable_offline_email_notifications', False)

def do_welcome_unsubscribe(__tmp2: __typ1) -> None:
    clear_scheduled_emails(__tmp2.id, ScheduledEmail.WELCOME)

def do_digest_unsubscribe(__tmp2: __typ1) :
    do_change_notification_settings(__tmp2, 'enable_digest_emails', False)

def __tmp3(__tmp2) :
    do_change_notification_settings(__tmp2, 'enable_login_emails', False)

# The keys are part of the URL for the unsubscribe link and must be valid
# without encoding.
# The values are a tuple of (display name, unsubscribe function), where the
# display name is what we call this class of email in user-visible text.
email_unsubscribers = {
    "missed_messages": ("missed messages", do_missedmessage_unsubscribe),
    "welcome": ("welcome", do_welcome_unsubscribe),
    "digest": ("digest", do_digest_unsubscribe),
    "login": ("login", __tmp3)
}

# Login NOT required. These are for one-click unsubscribes.
def email_unsubscribe(__tmp1: __typ0, email_type,
                      confirmation_key: <FILL>) :
    if email_type in email_unsubscribers:
        display_name, unsubscribe_function = email_unsubscribers[email_type]
        return __tmp0(__tmp1, confirmation_key, display_name, unsubscribe_function)

    return render(__tmp1, 'zerver/unsubscribe_link_error.html')
