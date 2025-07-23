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

def __tmp2(__tmp4: <FILL>) :

    # Check that this service is present in EMBEDDED_BOTS, add exception handling.
    is_present_in_registry = any(__tmp4 == embedded_bot_service.name for
                                 embedded_bot_service in EMBEDDED_BOTS)
    if not is_present_in_registry:
        return None
    bot_module_name = 'zulip_bots.bots.%s.%s' % (__tmp4, __tmp4)
    bot_module = importlib.import_module(bot_module_name)  # type: Any
    return bot_module.handler_class()


class StateHandler:
    storage_size_limit = 10000000   # type: int # TODO: Store this in the server configuration model.

    def __init__(__tmp1, user_profile) -> None:
        __tmp1.user_profile = user_profile
        __tmp1.marshal = lambda obj: json.dumps(obj)
        __tmp1.demarshal = lambda obj: json.loads(obj)

    def get(__tmp1, key) :
        return __tmp1.demarshal(get_bot_storage(__tmp1.user_profile, key))

    def __tmp6(__tmp1, key: str, __tmp3) -> None:
        set_bot_storage(__tmp1.user_profile, [(key, __tmp1.marshal(__tmp3))])

    def remove(__tmp1, key) -> None:
        remove_bot_storage(__tmp1.user_profile, [key])

    def __tmp7(__tmp1, key) -> bool:
        return is_key_in_bot_storage(__tmp1.user_profile, key)

class EmbeddedBotQuitException(Exception):
    pass

class EmbeddedBotHandler:
    def __init__(__tmp1, user_profile) :
        # Only expose a subset of our UserProfile's functionality
        __tmp1.user_profile = user_profile
        __tmp1._rate_limit = RateLimit(20, 5)
        __tmp1.full_name = user_profile.full_name
        __tmp1.email = user_profile.email
        __tmp1.storage = StateHandler(user_profile)

    def send_message(__tmp1, message: Dict[str, Any]) :
        if not __tmp1._rate_limit.is_legal():
            __tmp1._rate_limit.show_error_and_exit()

        if message['type'] == 'stream':
            internal_send_stream_message(__tmp1.user_profile.realm, __tmp1.user_profile, message['to'],
                                         message['topic'], message['content'])
            return

        assert message['type'] == 'private'
        # Ensure that it's a comma-separated list, even though the
        # usual 'to' field could be either a List[str] or a str.
        recipients = ','.join(message['to']).split(',')

        if len(message['to']) == 1:
            recipient_user = get_active_user(recipients[0], __tmp1.user_profile.realm)
            internal_send_private_message(__tmp1.user_profile.realm, __tmp1.user_profile,
                                          recipient_user, message['content'])
        else:
            internal_send_huddle_message(__tmp1.user_profile.realm, __tmp1.user_profile,
                                         recipients, message['content'])

    def __tmp0(__tmp1, message, response) :
        if message['type'] == 'private':
            __tmp1.send_message(dict(
                type='private',
                to=[x['email'] for x in message['display_recipient']],
                content=response,
                sender_email=message['sender_email'],
            ))
        else:
            __tmp1.send_message(dict(
                type='stream',
                to=message['display_recipient'],
                topic=get_topic_from_message_info(message),
                content=response,
                sender_email=message['sender_email'],
            ))

    # The bot_name argument exists only to comply with ExternalBotHandler.get_config_info().
    def get_config_info(__tmp1, __tmp5, optional: bool=False) -> Dict[str, str]:
        try:
            return get_bot_config(__tmp1.user_profile)
        except ConfigError:
            if optional:
                return dict()
            raise

    def quit(__tmp1, message: str= "") :
        raise EmbeddedBotQuitException(message)
