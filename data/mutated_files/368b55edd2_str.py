from typing import TypeAlias
__typ0 : TypeAlias = "Any"

from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.template import loader
from django.utils.timezone import \
    get_current_timezone_name as timezone_get_current_timezone_name
from django.utils.timezone import now as timezone_now
from django.utils.translation import ugettext_lazy as _

from confirmation.models import one_click_unsubscribe_link
from zerver.lib.queue import queue_json_publish
from zerver.lib.send_email import FromAddress
from zerver.models import UserProfile
from zerver.lib.timezone import get_timezone

JUST_CREATED_THRESHOLD = 60

def get_device_browser(__tmp1: <FILL>) -> Optional[str]:
    __tmp1 = __tmp1.lower()
    if "zulip" in __tmp1:
        return "Zulip"
    elif "edge" in __tmp1:
        return "Edge"
    elif "opera" in __tmp1 or "opr/" in __tmp1:
        return "Opera"
    elif ("chrome" in __tmp1 or "crios" in __tmp1) and "chromium" not in __tmp1:
        return 'Chrome'
    elif "firefox" in __tmp1 and "seamonkey" not in __tmp1 and "chrome" not in __tmp1:
        return "Firefox"
    elif "chromium" in __tmp1:
        return "Chromium"
    elif "safari" in __tmp1 and "chrome" not in __tmp1 and "chromium" not in __tmp1:
        return "Safari"
    elif "msie" in __tmp1 or "trident" in __tmp1:
        return "Internet Explorer"
    else:
        return None


def get_device_os(__tmp1) -> Optional[str]:
    __tmp1 = __tmp1.lower()
    if "windows" in __tmp1:
        return "Windows"
    elif "macintosh" in __tmp1:
        return "macOS"
    elif "linux" in __tmp1 and "android" not in __tmp1:
        return "Linux"
    elif "android" in __tmp1:
        return "Android"
    elif "ios" in __tmp1:
        return "iOS"
    elif "like mac os x" in __tmp1:
        return "iOS"
    elif " cros " in __tmp1:
        return "ChromeOS"
    else:
        return None


@receiver(user_logged_in, dispatch_uid="only_on_login")
def __tmp2(__tmp3, user: UserProfile, __tmp0: __typ0, **kwargs) :
    if not user.enable_login_emails:
        return
    # We import here to minimize the dependencies of this module,
    # since it runs as part of `manage.py` initialization
    from zerver.context_processors import common_context

    if not settings.SEND_LOGIN_EMAILS:
        return

    if __tmp0:
        # If the user's account was just created, avoid sending an email.
        if (timezone_now() - user.date_joined).total_seconds() <= JUST_CREATED_THRESHOLD:
            return

        __tmp1 = __tmp0.META.get('HTTP_USER_AGENT', "").lower()

        context = common_context(user)
        context['user_email'] = user.email
        user_tz = user.timezone
        if user_tz == '':
            user_tz = timezone_get_current_timezone_name()
        local_time = timezone_now().astimezone(get_timezone(user_tz))
        if user.twenty_four_hour_time:
            hhmm_string = local_time.strftime('%H:%M')
        else:
            hhmm_string = local_time.strftime('%I:%M%p')
        context['login_time'] = local_time.strftime('%A, %B %d, %Y at {} %Z'.format(hhmm_string))
        context['device_ip'] = __tmp0.META.get('REMOTE_ADDR') or _("Unknown IP address")
        context['device_os'] = get_device_os(__tmp1)
        context['device_browser'] = get_device_browser(__tmp1)
        context['unsubscribe_link'] = one_click_unsubscribe_link(user, 'login')

        email_dict = {
            'template_prefix': 'zerver/emails/notify_new_login',
            'to_user_id': user.id,
            'from_name': 'Zulip Account Security',
            'from_address': FromAddress.NOREPLY,
            'context': context}
        queue_json_publish("email_senders", email_dict)
