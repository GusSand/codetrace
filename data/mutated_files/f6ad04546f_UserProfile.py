from typing import TypeAlias
__typ0 : TypeAlias = "QuerySet"
__typ1 : TypeAlias = "int"
from typing import Dict, List, Tuple
from mypy_extensions import TypedDict

from django.db.models.query import QuerySet
from zerver.models import (
    Recipient,
    Stream,
    Subscription,
    UserProfile,
)

def get_active_subscriptions_for_stream_id(__tmp2: __typ1) -> __typ0:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        recipient__type=Recipient.STREAM,
        recipient__type_id=__tmp2,
        active=True,
    )

def get_active_subscriptions_for_stream_ids(__tmp0) -> __typ0:
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        recipient__type=Recipient.STREAM,
        recipient__type_id__in=__tmp0,
        active=True
    )

def __tmp3(user_profile: <FILL>) :
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        user_profile=user_profile,
        recipient__type=Recipient.STREAM,
    )

def __tmp1(user_profiles) :
    # TODO: Change return type to QuerySet[Subscription]
    return Subscription.objects.filter(
        user_profile__in=user_profiles,
        recipient__type=Recipient.STREAM,
    )

SubInfo = TypedDict('SubInfo', {
    'sub': Subscription,
    'stream': Stream,
})

def get_bulk_stream_subscriber_info(
        user_profiles: List[UserProfile],
        stream_dict) -> Dict[__typ1, List[Tuple[Subscription, Stream]]]:

    __tmp0 = stream_dict.keys()

    result = {
        user_profile.id: []
        for user_profile in user_profiles
    }  # type: Dict[int, List[Tuple[Subscription, Stream]]]

    subs = Subscription.objects.filter(
        user_profile__in=user_profiles,
        recipient__type=Recipient.STREAM,
        recipient__type_id__in=__tmp0,
        active=True,
    ).select_related('user_profile', 'recipient')

    for sub in subs:
        user_profile_id = sub.user_profile_id
        __tmp2 = sub.recipient.type_id
        stream = stream_dict[__tmp2]
        result[user_profile_id].append((sub, stream))

    return result

def num_subscribers_for_stream_id(__tmp2) -> __typ1:
    return get_active_subscriptions_for_stream_id(__tmp2).filter(
        user_profile__is_active=True,
    ).count()
