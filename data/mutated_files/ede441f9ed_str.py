from typing import TypeAlias
__typ2 : TypeAlias = "UserProfile"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
"""Webhooks for external integrations."""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import ujson
from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import authenticated_rest_api_view
from zerver.lib.notifications import convert_html_to_markdown
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_error, json_success
from zerver.lib.webhooks.common import check_send_webhook_message
from zerver.models import UserProfile, get_client

class __typ0(Dict[str, __typ3]):
    """
    A helper class to turn a dictionary with ticket information into
    an object where each of the keys is an attribute for easy access.
    """

    def __tmp7(__tmp0, __tmp1: str) -> __typ3:
        if "_" in __tmp1:
            return __tmp0.get(__tmp1)
        else:
            return __tmp0.get("ticket_" + __tmp1)


def __tmp4(property: <FILL>, __tmp11: __typ1) -> str:
    """The Freshdesk API is currently pretty broken: statuses are customizable
    but the API will only tell you the number associated with the status, not
    the name. While we engage the Freshdesk developers about exposing this
    information through the API, since only FlightCar uses this integration,
    hardcode their statuses.
    """
    statuses = ["", "", "Open", "Pending", "Resolved", "Closed",
                "Waiting on Customer", "Job Application", "Monthly"]
    priorities = ["", "Low", "Medium", "High", "Urgent"]

    name = ""
    if property == "status":
        name = statuses[__tmp11] if __tmp11 < len(statuses) else str(__tmp11)
    elif property == "priority":
        name = priorities[__tmp11] if __tmp11 < len(priorities) else str(__tmp11)

    return name


def __tmp5(__tmp8) -> List[str]:
    """These are always of the form "{ticket_action:created}" or
    "{status:{from:4,to:6}}". Note the lack of string quoting: this isn't
    valid JSON so we have to parse it ourselves.
    """
    data = __tmp8.replace("{", "").replace("}", "").replace(",", ":").split(":")

    if len(data) == 2:
        # This is a simple ticket action event, like
        # {ticket_action:created}.
        return data
    else:
        # This is a property change event, like {status:{from:4,to:6}}. Pull out
        # the property, from, and to states.
        property, _, from_state, _, to_state = data
        return [property, __tmp4(property, __typ1(from_state)),
                __tmp4(property, __typ1(to_state))]


def format_freshdesk_note_message(__tmp3: __typ0, __tmp10: List[str]) -> str:
    """There are public (visible to customers) and private note types."""
    note_type = __tmp10[1]
    content = "%s <%s> added a %s note to [ticket #%s](%s)." % (
        __tmp3.requester_name, __tmp3.requester_email, note_type,
        __tmp3.id, __tmp3.url)

    return content


def __tmp9(__tmp3: __typ0, __tmp10: List[str]) -> str:
    """Freshdesk will only tell us the first event to match our webhook
    configuration, so if we change multiple properties, we only get the before
    and after data for the first one.
    """
    content = "%s <%s> updated [ticket #%s](%s):\n\n" % (
        __tmp3.requester_name, __tmp3.requester_email, __tmp3.id, __tmp3.url)
    # Why not `"%s %s %s" % event_info`? Because the linter doesn't like it.
    content += "%s: **%s** => **%s**" % (
        __tmp10[0].capitalize(), __tmp10[1], __tmp10[2])

    return content


def __tmp6(__tmp3: __typ0) -> str:
    """They send us the description as HTML."""
    cleaned_description = convert_html_to_markdown(__tmp3.description)
    content = "%s <%s> created [ticket #%s](%s):\n\n" % (
        __tmp3.requester_name, __tmp3.requester_email, __tmp3.id, __tmp3.url)
    content += """~~~ quote
%s
~~~\n
""" % (cleaned_description,)
    content += "Type: **%s**\nPriority: **%s**\nStatus: **%s**" % (
        __tmp3.type, __tmp3.priority, __tmp3.status)

    return content

@authenticated_rest_api_view(webhook_client_name="Freshdesk")
@has_request_variables
def __tmp12(request: HttpRequest, __tmp2: __typ2,
                          payload: Dict[str, __typ3]=REQ(argument_type='body')) -> HttpResponse:
    ticket_data = payload["freshdesk_webhook"]

    required_keys = [
        "triggered_event", "ticket_id", "ticket_url", "ticket_type",
        "ticket_subject", "ticket_description", "ticket_status",
        "ticket_priority", "requester_name", "requester_email",
    ]

    for key in required_keys:
        if ticket_data.get(key) is None:
            logging.warning("Freshdesk webhook error. Payload was:")
            logging.warning(request.body)
            return json_error(_("Missing key %s in JSON") % (key,))

    __tmp3 = __typ0(ticket_data)

    subject = "#%s: %s" % (__tmp3.id, __tmp3.subject)
    __tmp10 = __tmp5(__tmp3.triggered_event)

    if __tmp10[1] == "created":
        content = __tmp6(__tmp3)
    elif __tmp10[0] == "note_type":
        content = format_freshdesk_note_message(__tmp3, __tmp10)
    elif __tmp10[0] in ("status", "priority"):
        content = __tmp9(__tmp3, __tmp10)
    else:
        # Not an event we know handle; do nothing.
        return json_success()

    check_send_webhook_message(request, __tmp2, subject, content)
    return json_success()
