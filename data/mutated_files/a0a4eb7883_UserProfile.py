from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
from django.conf import settings
from django.db.models import Sum
from django.db.models.query import F
from django.db.models.functions import Length
from zerver.models import BotStorageData, UserProfile, Length

from typing import Optional, List, Tuple

class StateError(Exception):
    pass

def get_bot_storage(__tmp3, __tmp5: __typ0) -> __typ0:
    try:
        return BotStorageData.objects.get(__tmp3=__tmp3, __tmp5=__tmp5).value
    except BotStorageData.DoesNotExist:
        raise StateError("Key does not exist.")

def __tmp0(__tmp3: UserProfile, __tmp5: Optional[__typ0]=None) -> int:
    if __tmp5 is None:
        return BotStorageData.objects.filter(__tmp3=__tmp3) \
                                     .annotate(key_size=Length('key'), value_size=Length('value')) \
                                     .aggregate(sum=Sum(F('key_size')+F('value_size')))['sum'] or 0
    else:
        try:
            return len(__tmp5) + len(BotStorageData.objects.get(__tmp3=__tmp3, __tmp5=__tmp5).value)
        except BotStorageData.DoesNotExist:
            return 0

def set_bot_storage(__tmp3: UserProfile, entries: List[Tuple[__typ0, __typ0]]) -> None:
    storage_size_limit = settings.USER_STATE_SIZE_LIMIT
    storage_size_difference = 0
    for __tmp5, value in entries:
        if type(__tmp5) is not __typ0:
            raise StateError("Key type is {}, but should be str.".format(type(__tmp5)))
        if type(value) is not __typ0:
            raise StateError("Value type is {}, but should be str.".format(type(value)))
        storage_size_difference += (len(__tmp5) + len(value)) - __tmp0(__tmp3, __tmp5)
    new_storage_size = __tmp0(__tmp3) + storage_size_difference
    if new_storage_size > storage_size_limit:
        raise StateError("Request exceeds storage limit by {} characters. The limit is {} characters."
                         .format(new_storage_size - storage_size_limit, storage_size_limit))
    else:
        for __tmp5, value in entries:
            BotStorageData.objects.update_or_create(__tmp3=__tmp3, __tmp5=__tmp5,
                                                    defaults={'value': value})

def remove_bot_storage(__tmp3: <FILL>, __tmp2: List[__typ0]) -> None:
    queryset = BotStorageData.objects.filter(__tmp3=__tmp3, key__in=__tmp2)
    if len(queryset) < len(__tmp2):
        raise StateError("Key does not exist.")
    queryset.delete()

def __tmp4(__tmp3: UserProfile, __tmp5: __typ0) -> __typ1:
    return BotStorageData.objects.filter(__tmp3=__tmp3, __tmp5=__tmp5).exists()

def __tmp1(__tmp3: UserProfile) -> List[__typ0]:
    return list(BotStorageData.objects.filter(__tmp3=__tmp3).values_list('key', flat=True))
