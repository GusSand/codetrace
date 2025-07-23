from typing import TypeAlias
__typ0 : TypeAlias = "QuerySet"
from typing import Dict, List, Tuple
from mypy_extensions import TypedDict

from django.db.models.query import QuerySet
from zerver.models import (
    Recipient,
    Stream,
    Subscription,
    UserProfile,
)

def get_active_subscriptions_for_stream_id(__tmp3: <FILL>) -> __typ0:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        recipient__type=Recipient.STREAM,
        recipient__type_id=__tmp3,
        active=True,
    )

def __tmp4(__tmp0: List[int]) -> __typ0:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        recipient__type=Recipient.STREAM,
        recipient__type_id__in=__tmp0,
        active=True
    )

def __tmp6(user_profile) -> __typ0:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        user_profile=user_profile,
        recipient__type=Recipient.STREAM,
    )

def get_stream_subscriptions_for_users(__tmp1: List[UserProfile]) -> __typ0:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        user_profile__in=__tmp1,
        recipient__type=Recipient.STREAM,
    )

SubInfo = TypedDict('SubInfo', {
    'sub': Subscription,
    'stream': Stream,
})

def __tmp2(
        __tmp1: List[UserProfile],
        stream_dict: Dict[int, Stream]) -> Dict[int, List[Tuple[Subscription, Stream]]]:

    __tmp0 = stream_dict.keys()

    result = {
        user_profile.id: []
        for user_profile in __tmp1
    }  # type: Dict[int, List[Tuple[Subscription, Stream]]]

    subs = Subscription.objects.filter(
        user_profile__in=__tmp1,
        recipient__type=Recipient.STREAM,
        recipient__type_id__in=__tmp0,
        active=True,
    ).select_related('user_profile', 'recipient')

    for sub in subs:
        user_profile_id = sub.user_profile_id
        __tmp3 = sub.recipient.type_id
        stream = stream_dict[__tmp3]
        result[user_profile_id].append((sub, stream))

    return result

def __tmp5(__tmp3: int) -> int:
    return get_active_subscriptions_for_stream_id(__tmp3).filter(
        user_profile__is_active=True,
    ).count()
