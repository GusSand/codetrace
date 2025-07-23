from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
from django.conf import settings
from django.db.models import Sum
from django.db.models.query import F
from django.db.models.functions import Length
from zerver.models import BotStorageData, UserProfile, Length

from typing import Optional, List, Tuple

class StateError(Exception):
    pass

def get_bot_storage(__tmp2: UserProfile, key) -> __typ1:
    try:
        return BotStorageData.objects.get(__tmp2=__tmp2, key=key).value
    except BotStorageData.DoesNotExist:
        raise StateError("Key does not exist.")

def get_bot_storage_size(__tmp2: UserProfile, key: Optional[__typ1]=None) :
    if key is None:
        return BotStorageData.objects.filter(__tmp2=__tmp2) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(key) + len(BotStorageData.objects.get(__tmp2=__tmp2, key=key).value)
        except BotStorageData.DoesNotExist:
            return 0

def __tmp3(__tmp2: UserProfile, __tmp4: List[Tuple[__typ1, __typ1]]) -> None:
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for key, value in __tmp4:
        if type(key) is not __typ1:
            raise StateError("Key type is {}, but should be str.".format(type(key)))
        if type(value) is not __typ1:
            raise StateError("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(key) + len(value)) - get_bot_storage_size(__tmp2, key)
    new_storage_size = get_bot_storage_size(__tmp2) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise StateError("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for key, value in __tmp4:
            BotStorageData.objects.update_or_create(__tmp2=__tmp2, key=key,
                                                    defaults={'value': value})

def remove_bot_storage(__tmp2: UserProfile, __tmp1: List[__typ1]) :
    queryset = BotStorageData.objects.filter(__tmp2=__tmp2, key__in=__tmp1)
    if len(queryset) < len(__tmp1):
        raise StateError("Key does not exist.")
    queryset.delete()

def is_key_in_bot_storage(__tmp2, key: __typ1) -> bool:
    return BotStorageData.objects.filter(__tmp2=__tmp2, key=key).exists()

def __tmp0(__tmp2: <FILL>) -> List[__typ1]:
    return list(BotStorageData.objects.filter(__tmp2=__tmp2).values_list('key', flat=True))
