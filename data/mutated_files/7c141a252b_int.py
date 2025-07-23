from typing import Dict, List, Tuple
from mypy_extensions import TypedDict

from django.db.models.query import QuerySet
from zerver.models import (
    Recipient,
    Stream,
    Subscription,
    UserProfile,
)

def get_active_subscriptions_for_stream_id(__tmp4: int) -> QuerySet:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        recipient__type=Recipient.STREAM,
        recipient__type_id=__tmp4,
        active=True,
    )

def __tmp5(stream_ids) :
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        recipient__type=Recipient.STREAM,
        recipient__type_id__in=stream_ids,
        active=True
    )

def get_stream_subscriptions_for_user(__tmp3) :
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        __tmp3=__tmp3,
        recipient__type=Recipient.STREAM,
    )

def __tmp1(user_profiles) -> QuerySet:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        user_profile__in=user_profiles,
        recipient__type=Recipient.STREAM,
    )

SubInfo = TypedDict('SubInfo', {
    'sub': Subscription,
    'stream': Stream,
})

def __tmp2(
        user_profiles: List[UserProfile],
        __tmp0) -> Dict[int, List[Tuple[Subscription, Stream]]]:

    stream_ids = __tmp0.keys()

    result = {
        __tmp3.id: []
        for __tmp3 in user_profiles
    }  # type: Dict[int, List[Tuple[Subscription, Stream]]]

    subs = Subscription.objects.filter(
        user_profile__in=user_profiles,
        recipient__type=Recipient.STREAM,
        recipient__type_id__in=stream_ids,
        active=True,
    ).select_related('user_profile', 'recipient')

    for sub in subs:
        user_profile_id = sub.user_profile_id
        __tmp4 = sub.recipient.type_id
        stream = __tmp0[__tmp4]
        result[user_profile_id].append((sub, stream))

    return result

def __tmp6(__tmp4: <FILL>) :
    return get_active_subscriptions_for_stream_id(__tmp4).filter(
        user_profile__is_active=True,
    ).count()
