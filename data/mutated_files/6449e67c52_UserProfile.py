from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Callable

from confirmation.models import Confirmation, get_object_from_key, \
    render_confirmation_key_error, ConfirmationKeyException
from zerver.lib.actions import do_change_notification_settings, clear_scheduled_emails
from zerver.models import UserProfile, ScheduledEmail
from zerver.context_processors import common_context

def __tmp0(__tmp6, confirmation_key, __tmp1,
                        __tmp5) -> __typ0:
    try:
        __tmp3 = get_object_from_key(confirmation_key, Confirmation.UNSUBSCRIBE)
    except ConfirmationKeyException:
        return render(__tmp6, 'zerver/unsubscribe_link_error.html')

    __tmp5(__tmp3)
    context = common_context(__tmp3)
    context.update({"subscription_type": __tmp1})
    return render(__tmp6, 'zerver/unsubscribe_success.html', context=context)

# Email unsubscribe functions. All have the function signature
# processor(user_profile).

def __tmp8(__tmp3: <FILL>) -> None:
    do_change_notification_settings(__tmp3, 'enable_offline_email_notifications', False)

def __tmp2(__tmp3) :
    clear_scheduled_emails(__tmp3.id, ScheduledEmail.WELCOME)

def __tmp10(__tmp3) :
    do_change_notification_settings(__tmp3, 'enable_digest_emails', False)

def __tmp9(__tmp3) -> None:
    do_change_notification_settings(__tmp3, 'enable_login_emails', False)

# The keys are part of the URL for the unsubscribe link and must be valid
# without encoding.
# The values are a tuple of (display name, unsubscribe function), where the
# display name is what we call this class of email in user-visible text.
email_unsubscribers = {
    "missed_messages": ("missed messages", __tmp8),
    "welcome": ("welcome", __tmp2),
    "digest": ("digest", __tmp10),
    "login": ("login", __tmp9)
}

# Login NOT required. These are for one-click unsubscribes.
def __tmp4(__tmp6, __tmp7: str,
                      confirmation_key) :
    if __tmp7 in email_unsubscribers:
        display_name, __tmp5 = email_unsubscribers[__tmp7]
        return __tmp0(__tmp6, confirmation_key, display_name, __tmp5)

    return render(__tmp6, 'zerver/unsubscribe_link_error.html')
