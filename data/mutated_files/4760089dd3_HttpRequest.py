from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
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

def __tmp0(__tmp6: <FILL>, confirmation_key, __tmp1,
                        unsubscribe_function) -> __typ2:
    try:
        __tmp3 = get_object_from_key(confirmation_key, Confirmation.UNSUBSCRIBE)
    except ConfirmationKeyException:
        return render(__tmp6, 'zerver/unsubscribe_link_error.html')

    unsubscribe_function(__tmp3)
    context = common_context(__tmp3)
    context.update({"subscription_type": __tmp1})
    return render(__tmp6, 'zerver/unsubscribe_success.html', context=context)

# Email unsubscribe functions. All have the function signature
# processor(user_profile).

def do_missedmessage_unsubscribe(__tmp3) :
    do_change_notification_settings(__tmp3, 'enable_offline_email_notifications', False)

def __tmp2(__tmp3: __typ1) :
    clear_scheduled_emails(__tmp3.id, ScheduledEmail.WELCOME)

def __tmp7(__tmp3) :
    do_change_notification_settings(__tmp3, 'enable_digest_emails', False)

def do_login_unsubscribe(__tmp3: __typ1) :
    do_change_notification_settings(__tmp3, 'enable_login_emails', False)

# The keys are part of the URL for the unsubscribe link and must be valid
# without encoding.
# The values are a tuple of (display name, unsubscribe function), where the
# display name is what we call this class of email in user-visible text.
email_unsubscribers = {
    "missed_messages": ("missed messages", do_missedmessage_unsubscribe),
    "welcome": ("welcome", __tmp2),
    "digest": ("digest", __tmp7),
    "login": ("login", do_login_unsubscribe)
}

# Login NOT required. These are for one-click unsubscribes.
def __tmp4(__tmp6, __tmp5,
                      confirmation_key) :
    if __tmp5 in email_unsubscribers:
        display_name, unsubscribe_function = email_unsubscribers[__tmp5]
        return __tmp0(__tmp6, confirmation_key, display_name, unsubscribe_function)

    return render(__tmp6, 'zerver/unsubscribe_link_error.html')
