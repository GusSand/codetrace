from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "bool"
from django.conf import settings
from django.db.models import Sum
from django.db.models.query import F
from django.db.models.functions import Length
from zerver.models import BotStorageData, UserProfile, Length

from typing import Optional, List, Tuple

class StateError(Exception):
    pass

def get_bot_storage(__tmp1, __tmp0: str) -> str:
    try:
        return BotStorageData.objects.get(__tmp1=__tmp1, __tmp0=__tmp0).value
    except BotStorageData.DoesNotExist:
        raise StateError("Key does not exist.")

def get_bot_storage_size(__tmp1: __typ0, __tmp0: Optional[str]=None) -> int:
    if __tmp0 is None:
        return BotStorageData.objects.filter(__tmp1=__tmp1) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(__tmp0) + len(BotStorageData.objects.get(__tmp1=__tmp1, __tmp0=__tmp0).value)
        except BotStorageData.DoesNotExist:
            return 0

def __tmp3(__tmp1, entries) -> None:
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for __tmp0, value in entries:
        if type(__tmp0) is not str:
            raise StateError("Key type is {}, but should be str.".format(type(__tmp0)))
        if type(value) is not str:
            raise StateError("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(__tmp0) + len(value)) - get_bot_storage_size(__tmp1, __tmp0)
    new_storage_size = get_bot_storage_size(__tmp1) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise StateError("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for __tmp0, value in entries:
            BotStorageData.objects.update_or_create(__tmp1=__tmp1, __tmp0=__tmp0,
                                                    defaults={'value': value})

def remove_bot_storage(__tmp1: __typ0, keys: List[str]) -> None:
    queryset = BotStorageData.objects.filter(__tmp1=__tmp1, key__in=keys)
    if len(queryset) < len(keys):
        raise StateError("Key does not exist.")
    queryset.delete()

def __tmp2(__tmp1, __tmp0: <FILL>) -> __typ1:
    return BotStorageData.objects.filter(__tmp1=__tmp1, __tmp0=__tmp0).exists()

def get_keys_in_bot_storage(__tmp1: __typ0) :
    return list(BotStorageData.objects.filter(__tmp1=__tmp1).values_list('key', flat=True))
