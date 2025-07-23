from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ2 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "HttpResponse"

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Callable

from confirmation.models import Confirmation, get_object_from_key, \
    render_confirmation_key_error, ConfirmationKeyException
from zerver.lib.actions import do_change_notification_settings, clear_scheduled_emails
from zerver.models import UserProfile, ScheduledEmail
from zerver.context_processors import common_context

def __tmp0(request: __typ0, confirmation_key: str, __tmp1,
                        unsubscribe_function) :
    try:
        __tmp2 = get_object_from_key(confirmation_key, Confirmation.UNSUBSCRIBE)
    except ConfirmationKeyException:
        return render(request, 'zerver/unsubscribe_link_error.html')

    unsubscribe_function(__tmp2)
    context = common_context(__tmp2)
    context.update({"subscription_type": __tmp1})
    return render(request, 'zerver/unsubscribe_success.html', context=context)

# Email unsubscribe functions. All have the function signature
# processor(user_profile).

def __tmp3(__tmp2) :
    do_change_notification_settings(__tmp2, 'enable_offline_email_notifications', False)

def do_welcome_unsubscribe(__tmp2) -> None:
    clear_scheduled_emails(__tmp2.id, ScheduledEmail.WELCOME)

def __tmp5(__tmp2) :
    do_change_notification_settings(__tmp2, 'enable_digest_emails', False)

def __tmp4(__tmp2) :
    do_change_notification_settings(__tmp2, 'enable_login_emails', False)

# The keys are part of the URL for the unsubscribe link and must be valid
# without encoding.
# The values are a tuple of (display name, unsubscribe function), where the
# display name is what we call this class of email in user-visible text.
email_unsubscribers = {
    "missed_messages": ("missed messages", __tmp3),
    "welcome": ("welcome", do_welcome_unsubscribe),
    "digest": ("digest", __tmp5),
    "login": ("login", __tmp4)
}

# Login NOT required. These are for one-click unsubscribes.
def email_unsubscribe(request, email_type: <FILL>,
                      confirmation_key) -> __typ1:
    if email_type in email_unsubscribers:
        display_name, unsubscribe_function = email_unsubscribers[email_type]
        return __tmp0(request, confirmation_key, display_name, unsubscribe_function)

    return render(request, 'zerver/unsubscribe_link_error.html')
