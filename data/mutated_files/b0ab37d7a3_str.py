from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "HttpRequest"
# Webhooks for external integrations.
import ujson
from typing import Mapping, Any, Tuple, Optional
from django.utils.translation import ugettext as _
from django.http import HttpRequest, HttpResponse
from zerver.decorator import api_key_only_webhook_view, return_success_on_head_request
from zerver.lib.response import json_success, json_error
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.webhooks.common import check_send_webhook_message, \
    UnexpectedWebhookEventType
from zerver.models import UserProfile

from .card_actions import SUPPORTED_CARD_ACTIONS, process_card_action
from .board_actions import SUPPORTED_BOARD_ACTIONS, process_board_action
from .exceptions import UnsupportedAction

@api_key_only_webhook_view('Trello')
@return_success_on_head_request
@has_request_variables
def api_trello_webhook(request: __typ0,
                       user_profile: __typ1,
                       payload: Mapping[str, Any]=REQ(argument_type='body')) -> HttpResponse:
    payload = ujson.loads(request.body)
    action_type = payload['action'].get('type')
    try:
        message = __tmp0(payload, action_type)
        if message is None:
            return json_success()
        else:
            subject, body = message
    except UnsupportedAction:
        raise UnexpectedWebhookEventType('Trello', action_type)

    check_send_webhook_message(request, user_profile, subject, body)
    return json_success()

def __tmp0(payload: Mapping[str, Any], action_type: <FILL>) -> Optional[Tuple[str, str]]:
    if action_type in SUPPORTED_CARD_ACTIONS:
        return process_card_action(payload, action_type)
    if action_type in SUPPORTED_BOARD_ACTIONS:
        return process_board_action(payload, action_type)

    raise UnsupportedAction('{} if not supported'.format(action_type))
