from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
from django.conf import settings
from django.db.models import Sum
from django.db.models.query import F
from django.db.models.functions import Length
from zerver.models import BotStorageData, UserProfile, Length

from typing import Optional, List, Tuple

class StateError(Exception):
    pass

def get_bot_storage(__tmp3, __tmp7: <FILL>) :
    try:
        return BotStorageData.objects.get(__tmp3=__tmp3, __tmp7=__tmp7).value
    except BotStorageData.DoesNotExist:
        raise StateError("Key does not exist.")

def __tmp0(__tmp3, __tmp7: Optional[str]=None) :
    if __tmp7 is None:
        return BotStorageData.objects.filter(__tmp3=__tmp3) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(__tmp7) + len(BotStorageData.objects.get(__tmp3=__tmp3, __tmp7=__tmp7).value)
        except BotStorageData.DoesNotExist:
            return 0

def __tmp5(__tmp3, entries) :
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for __tmp7, value in entries:
        if type(__tmp7) is not str:
            raise StateError("Key type is {}, but should be str.".format(type(__tmp7)))
        if type(value) is not str:
            raise StateError("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(__tmp7) + len(value)) - __tmp0(__tmp3, __tmp7)
    new_storage_size = __tmp0(__tmp3) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise StateError("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for __tmp7, value in entries:
            BotStorageData.objects.update_or_create(__tmp3=__tmp3, __tmp7=__tmp7,
                                                    defaults={'value': value})

def __tmp6(__tmp3, __tmp2) :
    queryset = BotStorageData.objects.filter(__tmp3=__tmp3, key__in=__tmp2)
    if len(queryset) < len(__tmp2):
        raise StateError("Key does not exist.")
    queryset.delete()

def __tmp4(__tmp3, __tmp7) :
    return BotStorageData.objects.filter(__tmp3=__tmp3, __tmp7=__tmp7).exists()

def __tmp1(__tmp3) :
    return list(BotStorageData.objects.filter(__tmp3=__tmp3).values_list('key', flat=True))
