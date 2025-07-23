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

def get_bot_storage(__tmp2: UserProfile, __tmp6) :
    try:
        return BotStorageData.objects.get(__tmp2=__tmp2, __tmp6=__tmp6).value
    except BotStorageData.DoesNotExist:
        raise __typ3("Key does not exist.")

def __tmp0(__tmp2: UserProfile, __tmp6: Optional[__typ1]=None) :
    if __tmp6 is None:
        return BotStorageData.objects.filter(__tmp2=__tmp2) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(__tmp6) + len(BotStorageData.objects.get(__tmp2=__tmp2, __tmp6=__tmp6).value)
        except BotStorageData.DoesNotExist:
            return 0

def set_bot_storage(__tmp2: <FILL>, __tmp4: List[Tuple[__typ1, __typ1]]) :
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for __tmp6, value in __tmp4:
        if type(__tmp6) is not __typ1:
            raise __typ3("Key type is {}, but should be str.".format(type(__tmp6)))
        if type(value) is not __typ1:
            raise __typ3("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(__tmp6) + len(value)) - __tmp0(__tmp2, __tmp6)
    new_storage_size = __tmp0(__tmp2) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise __typ3("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for __tmp6, value in __tmp4:
            BotStorageData.objects.update_or_create(__tmp2=__tmp2, __tmp6=__tmp6,
                                                    defaults={'value': value})

def __tmp5(__tmp2, keys) -> None:
    queryset = BotStorageData.objects.filter(__tmp2=__tmp2, key__in=keys)
    if len(queryset) < len(keys):
        raise __typ3("Key does not exist.")
    queryset.delete()

def __tmp3(__tmp2: UserProfile, __tmp6: __typ1) :
    return BotStorageData.objects.filter(__tmp2=__tmp2, __tmp6=__tmp6).exists()

def __tmp1(__tmp2: UserProfile) :
    return list(BotStorageData.objects.filter(__tmp2=__tmp2).values_list('key', flat=True))
