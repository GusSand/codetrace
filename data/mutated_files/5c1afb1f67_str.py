from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
from django.conf import settings
from django.db.models import Sum
from django.db.models.query import F
from django.db.models.functions import Length
from zerver.models import BotConfigData, UserProfile

from typing import List, Dict, Optional

from collections import defaultdict

import os

import configparser
import importlib

class __typ0(Exception):
    pass

def get_bot_config(bot_profile) -> Dict[str, str]:
    entries = BotConfigData.objects.filter(bot_profile=bot_profile)
    if not entries:
        raise __typ0("No config data available.")
    return {entry.key: entry.value for entry in entries}

def __tmp2(bot_profile_ids: List[int]) -> Dict[int, Dict[str, str]]:
    if not bot_profile_ids:
        return {}
    entries = BotConfigData.objects.filter(bot_profile_id__in=bot_profile_ids)
    entries_by_uid = defaultdict(dict)  # type: Dict[int, Dict[str, str]]
    for entry in entries:
        entries_by_uid[entry.bot_profile_id].update({entry.key: entry.value})
    return entries_by_uid

def __tmp1(bot_profile, key: Optional[str]=None) -> int:
    if key is None:
        return BotConfigData.objects.filter(bot_profile=bot_profile) \
                                    .annotate(key_size=Length('key'), value_size=Length('value')) \
                                    .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(key) + len(BotConfigData.objects.get(bot_profile=bot_profile, key=key).value)
        except BotConfigData.DoesNotExist:
            return 0

def set_bot_config(bot_profile: __typ1, key: <FILL>, value: str) :
    config_size_limit = settings.BOT_CONFIG_SIZE_LIMIT
    old_entry_size = __tmp1(bot_profile, key)
    new_entry_size = len(key) + len(value)
    old_config_size = __tmp1(bot_profile)
    new_config_size = old_config_size + (new_entry_size - old_entry_size)
    if new_config_size > config_size_limit:
        raise __typ0("Cannot store configuration. Request would require {} characters. "
                          "The current configuration size limit is {} characters.".format(new_config_size,
                                                                                          config_size_limit))
    obj, created = BotConfigData.objects.get_or_create(bot_profile=bot_profile, key=key,
                                                       defaults={'value': value})
    if not created:
        obj.value = value
        obj.save()

def load_bot_config_template(__tmp0: str) -> Dict[str, str]:
    bot_module_name = 'zulip_bots.bots.{}'.format(__tmp0)
    bot_module = importlib.import_module(bot_module_name)
    bot_module_path = os.path.dirname(bot_module.__file__)
    config_path = os.path.join(bot_module_path, '{}.conf'.format(__tmp0))
    if os.path.isfile(config_path):
        config = configparser.ConfigParser()
        with open(config_path) as conf:
            config.readfp(conf)  # type: ignore # readfp->read_file in python 3, so not in stubs
        return dict(config.items(__tmp0))
    else:
        return dict()
