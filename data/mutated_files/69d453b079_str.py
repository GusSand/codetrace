from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "Any"
import json
import logging
import os
import signal
import sys
import time
import re
import importlib
from zerver.lib.actions import internal_send_private_message, \
    internal_send_stream_message, internal_send_huddle_message
from zerver.models import UserProfile, get_active_user
from zerver.lib.bot_storage import get_bot_storage, set_bot_storage, \
    is_key_in_bot_storage, get_bot_storage_size, remove_bot_storage
from zerver.lib.bot_config import get_bot_config, ConfigError
from zerver.lib.integrations import EMBEDDED_BOTS
from zerver.lib.topic import get_topic_from_message_info

import configparser

if False:
    from mypy_extensions import NoReturn
from typing import Any, Optional, List, Dict
from types import ModuleType

our_dir = os.path.dirname(os.path.abspath(__file__))

from zulip_bots.lib import RateLimit

def get_bot_handler(service_name: str) -> __typ2:

    # Check that this service is present in EMBEDDED_BOTS, add exception handling.
    is_present_in_registry = any(service_name == embedded_bot_service.name for
                                 embedded_bot_service in EMBEDDED_BOTS)
    if not is_present_in_registry:
        return None
    bot_module_name = 'zulip_bots.bots.%s.%s' % (service_name, service_name)
    bot_module = importlib.import_module(bot_module_name)  # type: Any
    return bot_module.handler_class()


class StateHandler:
    storage_size_limit = 10000000   # type: int # TODO: Store this in the server configuration model.

    def __tmp1(__tmp0, user_profile: __typ0) -> None:
        __tmp0.user_profile = user_profile
        __tmp0.marshal = lambda obj: json.dumps(obj)
        __tmp0.demarshal = lambda obj: json.loads(obj)

    def get(__tmp0, key: str) -> str:
        return __tmp0.demarshal(get_bot_storage(__tmp0.user_profile, key))

    def put(__tmp0, key: <FILL>, value: str) -> None:
        set_bot_storage(__tmp0.user_profile, [(key, __tmp0.marshal(value))])

    def remove(__tmp0, key) -> None:
        remove_bot_storage(__tmp0.user_profile, [key])

    def contains(__tmp0, key: str) -> bool:
        return is_key_in_bot_storage(__tmp0.user_profile, key)

class __typ1(Exception):
    pass

class EmbeddedBotHandler:
    def __tmp1(__tmp0, user_profile: __typ0) -> None:
        # Only expose a subset of our UserProfile's functionality
        __tmp0.user_profile = user_profile
        __tmp0._rate_limit = RateLimit(20, 5)
        __tmp0.full_name = user_profile.full_name
        __tmp0.email = user_profile.email
        __tmp0.storage = StateHandler(user_profile)

    def send_message(__tmp0, message) :
        if not __tmp0._rate_limit.is_legal():
            __tmp0._rate_limit.show_error_and_exit()

        if message['type'] == 'stream':
            internal_send_stream_message(__tmp0.user_profile.realm, __tmp0.user_profile, message['to'],
                                         message['topic'], message['content'])
            return

        assert message['type'] == 'private'
        # Ensure that it's a comma-separated list, even though the
        # usual 'to' field could be either a List[str] or a str.
        recipients = ','.join(message['to']).split(',')

        if len(message['to']) == 1:
            recipient_user = get_active_user(recipients[0], __tmp0.user_profile.realm)
            internal_send_private_message(__tmp0.user_profile.realm, __tmp0.user_profile,
                                          recipient_user, message['content'])
        else:
            internal_send_huddle_message(__tmp0.user_profile.realm, __tmp0.user_profile,
                                         recipients, message['content'])

    def send_reply(__tmp0, message, response: str) -> None:
        if message['type'] == 'private':
            __tmp0.send_message(dict(
                type='private',
                to=[x['email'] for x in message['display_recipient']],
                content=response,
                sender_email=message['sender_email'],
            ))
        else:
            __tmp0.send_message(dict(
                type='stream',
                to=message['display_recipient'],
                topic=get_topic_from_message_info(message),
                content=response,
                sender_email=message['sender_email'],
            ))

    # The bot_name argument exists only to comply with ExternalBotHandler.get_config_info().
    def get_config_info(__tmp0, bot_name, optional: bool=False) -> Dict[str, str]:
        try:
            return get_bot_config(__tmp0.user_profile)
        except ConfigError:
            if optional:
                return dict()
            raise

    def quit(__tmp0, message: str= "") -> None:
        raise __typ1(message)
