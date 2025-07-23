from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "HttpRequest"
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

def notify_bot_owner_about_invalid_json(__tmp2: __typ1,
                                        webhook_client_name: str) -> None:
    send_rate_limited_pm_notification_to_bot_owner(
        __tmp2, __tmp2.realm,
        INVALID_JSON_MESSAGE.format(webhook_name=webhook_client_name).strip()
    )

class __typ2(JsonableError):
    code = ErrorCode.UNEXPECTED_WEBHOOK_EVENT_TYPE
    data_fields = ['webhook_name', 'event_type']

    def __tmp3(__tmp1, webhook_name: <FILL>, event_type) :
        __tmp1.webhook_name = webhook_name
        __tmp1.event_type = event_type

    @staticmethod
    def __tmp0() :
        return _("The '{event_type}' event isn't currently supported by the {webhook_name} webhook")

class MissingHTTPEventHeader(JsonableError):
    code = ErrorCode.MISSING_HTTP_EVENT_HEADER
    data_fields = ['header']

    def __tmp3(__tmp1, header) :
        __tmp1.header = header

    @staticmethod
    def __tmp0() :
        return _("Missing the HTTP event header '{header}'")

@has_request_variables
def __tmp5(
        request, __tmp2,
        topic: str, body: str, stream: Optional[str]=REQ(default=None),
        user_specified_topic: Optional[str]=REQ("topic", default=None),
        unquote_stream: Optional[bool]=False
) :

    if stream is None:
        assert __tmp2.bot_owner is not None
        check_send_private_message(__tmp2, request.client,
                                   __tmp2.bot_owner, body)
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
            check_send_stream_message(__tmp2, request.client,
                                      stream, topic, body)
        except StreamDoesNotExistError:
            # A PM will be sent to the bot_owner by check_message, notifying
            # that the webhook bot just tried to send a message to a non-existent
            # stream, so we don't need to re-raise it since it clutters up
            # webhook-errors.log
            pass

def __tmp4(request: __typ0, header: str,
                                         __tmp6: str) :
    extracted_header = request.META.get(DJANGO_HTTP_PREFIX + header)
    if extracted_header is None:
        message_body = MISSING_EVENT_HEADER_MESSAGE.format(
            bot_name=request.user.full_name,
            request_path=request.path,
            header_name=header,
            __tmp6=__tmp6,
            support_email=FromAddress.SUPPORT,
        )
        send_rate_limited_pm_notification_to_bot_owner(
            request.user, request.user.realm, message_body)

        raise MissingHTTPEventHeader(header)

    return extracted_header
