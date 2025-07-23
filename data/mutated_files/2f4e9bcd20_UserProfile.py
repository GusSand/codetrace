from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
from django.conf import settings
from django.db.models import Sum
from django.db.models.query import F
from django.db.models.functions import Length
from zerver.models import BotStorageData, UserProfile, Length

from typing import Optional, List, Tuple

class __typ3(Exception):
    pass

def get_bot_storage(__tmp2: UserProfile, __tmp5: __typ1) -> __typ1:
    try:
        return BotStorageData.objects.get(__tmp2=__tmp2, __tmp5=__tmp5).value
    except BotStorageData.DoesNotExist:
        raise __typ3("Key does not exist.")

def __tmp0(__tmp2: UserProfile, __tmp5: Optional[__typ1]=None) -> __typ0:
    if __tmp5 is None:
        return BotStorageData.objects.filter(__tmp2=__tmp2) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(__tmp5) + len(BotStorageData.objects.get(__tmp2=__tmp2, __tmp5=__tmp5).value)
        except BotStorageData.DoesNotExist:
            return 0

def __tmp3(__tmp2: UserProfile, entries: List[Tuple[__typ1, __typ1]]) -> None:
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for __tmp5, value in entries:
        if type(__tmp5) is not __typ1:
            raise __typ3("Key type is {}, but should be str.".format(type(__tmp5)))
        if type(value) is not __typ1:
            raise __typ3("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(__tmp5) + len(value)) - __tmp0(__tmp2, __tmp5)
    new_storage_size = __tmp0(__tmp2) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise __typ3("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for __tmp5, value in entries:
            BotStorageData.objects.update_or_create(__tmp2=__tmp2, __tmp5=__tmp5,
                                                    defaults={'value': value})

def remove_bot_storage(__tmp2: UserProfile, __tmp1: List[__typ1]) -> None:
    queryset = BotStorageData.objects.filter(__tmp2=__tmp2, key__in=__tmp1)
    if len(queryset) < len(__tmp1):
        raise __typ3("Key does not exist.")
    queryset.delete()

def __tmp4(__tmp2: <FILL>, __tmp5) :
    return BotStorageData.objects.filter(__tmp2=__tmp2, __tmp5=__tmp5).exists()

def get_keys_in_bot_storage(__tmp2: UserProfile) :
    return list(BotStorageData.objects.filter(__tmp2=__tmp2).values_list('key', flat=True))
