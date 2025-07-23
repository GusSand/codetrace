from typing import TypeAlias
__typ3 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "str"
from urllib.parse import unquote

from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import ugettext as _
from typing import Optional

from zerver.lib.actions import check_send_stream_message, \
    check_send_private_message, send_rate_limited_pm_notification_to_bot_owner
from zerver.lib.exceptions import StreamDoesNotExistError, JsonableError, \
    ErrorCode
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.send_email import FromAddress
from zerver.models import UserProfile, get_system_bot


MISSING_EVENT_HEADER_MESSAGE = """
Hi there!  Your bot {bot_name} just sent an HTTP request to {request_path} that
is missing the HTTP {header_name} header.  Because this header is how
{integration_name} indicates the event type, this usually indicates a configuration
issue, where you either entered the URL for a different integration, or are running
an older version of the third-party service that doesn't provide that header.
Contact {support_email} if you need help debugging!
"""

INVALID_JSON_MESSAGE = """
Hi there! It looks like you tried to setup the Zulip {webhook_name} integration,
but didn't correctly configure the webhook to send data in the JSON format
that this integration expects!
"""

# Django prefixes all custom HTTP headers with `HTTP_`
DJANGO_HTTP_PREFIX = "HTTP_"

def notify_bot_owner_about_invalid_json(user_profile: __typ3,
                                        webhook_client_name: __typ1) -> None:
    send_rate_limited_pm_notification_to_bot_owner(
        user_profile, user_profile.realm,
        INVALID_JSON_MESSAGE.format(webhook_name=webhook_client_name).strip()
    )

class __typ2(JsonableError):
    code = ErrorCode.UNEXPECTED_WEBHOOK_EVENT_TYPE
    data_fields = ['webhook_name', 'event_type']

    def __tmp2(__tmp1, webhook_name, event_type: Optional[__typ1]) -> None:
        __tmp1.webhook_name = webhook_name
        __tmp1.event_type = event_type

    @staticmethod
    def __tmp0() -> __typ1:
        return _("The '{event_type}' event isn't currently supported by the {webhook_name} webhook")

class __typ0(JsonableError):
    code = ErrorCode.MISSING_HTTP_EVENT_HEADER
    data_fields = ['header']

    def __tmp2(__tmp1, header: __typ1) -> None:
        __tmp1.header = header

    @staticmethod
    def __tmp0() -> __typ1:
        return _("Missing the HTTP event header '{header}'")

@has_request_variables
def check_send_webhook_message(
        request, user_profile: __typ3,
        topic, body: __typ1, stream: Optional[__typ1]=REQ(default=None),
        user_specified_topic: Optional[__typ1]=REQ("topic", default=None),
        unquote_stream: Optional[bool]=False
) -> None:

    if stream is None:
        assert user_profile.bot_owner is not None
        check_send_private_message(user_profile, request.client,
                                   user_profile.bot_owner, body)
    else:
        # Some third-party websites (such as Atlassian's JIRA), tend to
        # double escape their URLs in a manner that escaped space characters
        # (%20) are never properly decoded. We work around that by making sure
        # that the stream name is decoded on our end.
        if unquote_stream:
            stream = unquote(stream)

        if user_specified_topic is not None:
            topic = user_specified_topic

        try:
            check_send_stream_message(user_profile, request.client,
                                      stream, topic, body)
        except StreamDoesNotExistError:
            # A PM will be sent to the bot_owner by check_message, notifying
            # that the webhook bot just tried to send a message to a non-existent
            # stream, so we don't need to re-raise it since it clutters up
            # webhook-errors.log
            pass

def validate_extract_webhook_http_header(request: <FILL>, header: __typ1,
                                         integration_name: __typ1) -> __typ1:
    extracted_header = request.META.get(DJANGO_HTTP_PREFIX + header)
    if extracted_header is None:
        message_body = MISSING_EVENT_HEADER_MESSAGE.format(
            bot_name=request.user.full_name,
            request_path=request.path,
            header_name=header,
            integration_name=integration_name,
            support_email=FromAddress.SUPPORT,
        )
        send_rate_limited_pm_notification_to_bot_owner(
            request.user, request.user.realm, message_body)

        raise __typ0(header)

    return extracted_header
