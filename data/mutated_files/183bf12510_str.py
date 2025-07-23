from typing import TypeAlias
__typ2 : TypeAlias = "HttpResponse"
__typ1 : TypeAlias = "HttpRequest"
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

class __typ0(Dict[str, Any]):
    """
    A helper class to turn a dictionary with ticket information into
    an object where each of the keys is an attribute for easy access.
    """

    def __getattr__(self, __tmp0: <FILL>) -> Any:
        if "_" in __tmp0:
            return self.get(__tmp0)
        else:
            return self.get("ticket_" + __tmp0)


def property_name(property, index: int) :
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
        name = statuses[index] if index < len(statuses) else str(index)
    elif property == "priority":
        name = priorities[index] if index < len(priorities) else str(index)

    return name


def parse_freshdesk_event(event_string: str) :
    """These are always of the form "{ticket_action:created}" or
    "{status:{from:4,to:6}}". Note the lack of string quoting: this isn't
    valid JSON so we have to parse it ourselves.
    """
    data = event_string.replace("{", "").replace("}", "").replace(",", ":").split(":")

    if len(data) == 2:
        # This is a simple ticket action event, like
        # {ticket_action:created}.
        return data
    else:
        # This is a property change event, like {status:{from:4,to:6}}. Pull out
        # the property, from, and to states.
        property, _, from_state, _, to_state = data
        return [property, property_name(property, int(from_state)),
                property_name(property, int(to_state))]


def format_freshdesk_note_message(__tmp2, event_info) -> str:
    """There are public (visible to customers) and private note types."""
    note_type = event_info[1]
    content = "%s <%s> added a %s note to [ticket #%s](%s)." % (
        __tmp2.requester_name, __tmp2.requester_email, note_type,
        __tmp2.id, __tmp2.url)

    return content


def __tmp4(__tmp2: __typ0, event_info) :
    """Freshdesk will only tell us the first event to match our webhook
    configuration, so if we change multiple properties, we only get the before
    and after data for the first one.
    """
    content = "%s <%s> updated [ticket #%s](%s):\n\n" % (
        __tmp2.requester_name, __tmp2.requester_email, __tmp2.id, __tmp2.url)
    # Why not `"%s %s %s" % event_info`? Because the linter doesn't like it.
    content += "%s: **%s** => **%s**" % (
        event_info[0].capitalize(), event_info[1], event_info[2])

    return content


def __tmp3(__tmp2) :
    """They send us the description as HTML."""
    cleaned_description = convert_html_to_markdown(__tmp2.description)
    content = "%s <%s> created [ticket #%s](%s):\n\n" % (
        __tmp2.requester_name, __tmp2.requester_email, __tmp2.id, __tmp2.url)
    content += """~~~ quote
%s
~~~\n
""" % (cleaned_description,)
    content += "Type: **%s**\nPriority: **%s**\nStatus: **%s**" % (
        __tmp2.type, __tmp2.priority, __tmp2.status)

    return content

@authenticated_rest_api_view(webhook_client_name="Freshdesk")
@has_request_variables
def __tmp5(request, __tmp1: UserProfile,
                          payload: Dict[str, Any]=REQ(argument_type='body')) :
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

    __tmp2 = __typ0(ticket_data)

    subject = "#%s: %s" % (__tmp2.id, __tmp2.subject)
    event_info = parse_freshdesk_event(__tmp2.triggered_event)

    if event_info[1] == "created":
        content = __tmp3(__tmp2)
    elif event_info[0] == "note_type":
        content = format_freshdesk_note_message(__tmp2, event_info)
    elif event_info[0] in ("status", "priority"):
        content = __tmp4(__tmp2, event_info)
    else:
        # Not an event we know handle; do nothing.
        return json_success()

    check_send_webhook_message(request, __tmp1, subject, content)
    return json_success()
