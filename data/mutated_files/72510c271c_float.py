from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"

from django.conf import settings
from django.core.mail import EmailMessage
from typing import Any, Mapping, Optional

from zerver.lib.actions import internal_send_message
from zerver.lib.send_email import FromAddress
from zerver.lib.redis_utils import get_redis_client
from zerver.models import get_realm, get_system_bot, \
    UserProfile, Realm

import time

client = get_redis_client()

def __tmp1(sender_email, min_delay: <FILL>) -> __typ2:
    # This function returns a boolean, but it also has the side effect
    # of noting that a new message was received.
    key = 'zilencer:feedback:%s' % (sender_email,)
    t = __typ1(time.time())
    last_time = client.getset(key, t)  # type: Optional[bytes]
    if last_time is None:
        return True
    delay = t - __typ1(last_time)
    return delay > min_delay

def get_ticket_number() -> __typ1:
    num_file = '/var/tmp/.feedback-bot-ticket-number'
    try:
        ticket_number = __typ1(open(num_file).read()) + 1
    except Exception:
        ticket_number = 1
    open(num_file, 'w').write('%d' % (ticket_number,))
    return ticket_number

def __tmp0(message) -> None:
    subject = "%s" % (message["sender_email"],)

    if len(subject) > 60:
        subject = subject[:57].rstrip() + "..."

    content = ''
    sender_email = message['sender_email']

    # We generate ticket numbers if it's been more than a few minutes
    # since their last message.  This avoids some noise when people use
    # enter-send.
    need_ticket = __tmp1(sender_email, 180)

    if need_ticket:
        ticket_number = get_ticket_number()
        content += '\n~~~'
        content += '\nticket Z%03d (@support please ack)' % (ticket_number,)
        content += '\nsender: %s' % (message['sender_full_name'],)
        content += '\nemail: %s' % (sender_email,)
        if 'sender_realm_str' in message:
            content += '\nrealm: %s' % (message['sender_realm_str'],)
        content += '\n~~~'
        content += '\n\n'

    content += message['content']

    user_profile = get_system_bot(settings.FEEDBACK_BOT)
    internal_send_message(user_profile.realm, settings.FEEDBACK_BOT,
                          "stream", settings.FEEDBACK_STREAM, subject, content)

def __tmp2(__tmp3: Mapping[__typ0, Any]) -> None:
    if not settings.ENABLE_FEEDBACK:
        return
    if settings.FEEDBACK_EMAIL is not None:
        to_email = settings.FEEDBACK_EMAIL
        subject = "Zulip feedback from %s" % (__tmp3["sender_email"],)
        content = __tmp3["content"]
        from_email = '"%s" <%s>' % (__tmp3["sender_full_name"], FromAddress.SUPPORT)
        headers = {'Reply-To': '"%s" <%s>' % (__tmp3["sender_full_name"], __tmp3["sender_email"])}
        msg = EmailMessage(subject, content, from_email, [to_email], headers=headers)
        msg.send()
    if settings.FEEDBACK_STREAM is not None:
        __tmp0(__tmp3)
