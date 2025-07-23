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

def get_bot_storage(__tmp3: UserProfile, __tmp8) -> __typ1:
    try:
        return BotStorageData.objects.get(__tmp3=__tmp3, __tmp8=__tmp8).value
    except BotStorageData.DoesNotExist:
        raise __typ3("Key does not exist.")

def __tmp0(__tmp3: <FILL>, __tmp8: Optional[__typ1]=None) :
    if __tmp8 is None:
        return BotStorageData.objects.filter(__tmp3=__tmp3) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(__tmp8) + len(BotStorageData.objects.get(__tmp3=__tmp3, __tmp8=__tmp8).value)
        except BotStorageData.DoesNotExist:
            return 0

def __tmp4(__tmp3, __tmp5: List[Tuple[__typ1, __typ1]]) :
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for __tmp8, value in __tmp5:
        if type(__tmp8) is not __typ1:
            raise __typ3("Key type is {}, but should be str.".format(type(__tmp8)))
        if type(value) is not __typ1:
            raise __typ3("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(__tmp8) + len(value)) - __tmp0(__tmp3, __tmp8)
    new_storage_size = __tmp0(__tmp3) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise __typ3("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for __tmp8, value in __tmp5:
            BotStorageData.objects.update_or_create(__tmp3=__tmp3, __tmp8=__tmp8,
                                                    defaults={'value': value})

def __tmp7(__tmp3: UserProfile, __tmp2) :
    queryset = BotStorageData.objects.filter(__tmp3=__tmp3, key__in=__tmp2)
    if len(queryset) < len(__tmp2):
        raise __typ3("Key does not exist.")
    queryset.delete()

def __tmp6(__tmp3, __tmp8) :
    return BotStorageData.objects.filter(__tmp3=__tmp3, __tmp8=__tmp8).exists()

def __tmp1(__tmp3: UserProfile) :
    return list(BotStorageData.objects.filter(__tmp3=__tmp3).values_list('key', flat=True))
