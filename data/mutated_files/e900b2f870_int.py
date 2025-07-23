from typing import Any, Callable, Dict, List, Optional

from zerver.lib.topic import (
    topic_match_sa,
)
from zerver.models import (
    get_stream_recipient,
    get_stream,
    MutedTopic,
    UserProfile
)
from sqlalchemy.sql import (
    and_,
    column,
    not_,
    or_,
    Selectable
)

def get_topic_mutes(__tmp0: UserProfile) -> List[List[str]]:
    rows = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp2['stream__name'], __tmp2['topic_name']]
        for __tmp2 in rows
    ]

def __tmp4(__tmp0: UserProfile, __tmp6: List[List[str]]) -> None:

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).delete()

    for stream_name, __tmp5 in __tmp6:
        stream = get_stream(stream_name, __tmp0.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp10(
            __tmp0=__tmp0,
            __tmp1=stream.id,
            __tmp11=recipient.id,
            __tmp5=__tmp5,
        )

def __tmp10(__tmp0: UserProfile, __tmp1: <FILL>, __tmp11, __tmp5) -> None:
    MutedTopic.objects.create(
        __tmp0=__tmp0,
        __tmp1=__tmp1,
        __tmp11=__tmp11,
        __tmp5=__tmp5,
    )

def __tmp8(__tmp0: UserProfile, __tmp1: int, __tmp5: str) :
    __tmp2 = MutedTopic.objects.get(
        __tmp0=__tmp0,
        __tmp1=__tmp1,
        topic_name__iexact=__tmp5
    )
    __tmp2.delete()

def __tmp7(__tmp0: UserProfile, __tmp1: int, __tmp5) -> bool:
    __tmp3 = MutedTopic.objects.filter(
        __tmp0=__tmp0,
        __tmp1=__tmp1,
        topic_name__iexact=__tmp5,
    ).exists()
    return __tmp3

def exclude_topic_mutes(conditions,
                        __tmp0,
                        __tmp1: Optional[int]) -> List[Selectable]:
    query = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    )

    if __tmp1 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp1=__tmp1)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return conditions

    def mute_cond(__tmp2: Dict[str, Any]) -> Selectable:
        __tmp11 = __tmp2['recipient_id']
        __tmp5 = __tmp2['topic_name']
        stream_cond = column("recipient_id") == __tmp11
        topic_cond = topic_match_sa(__tmp5)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(mute_cond, rows))))
    return conditions + [condition]

def __tmp9(__tmp0: UserProfile) :
    rows = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp2 in rows:
        __tmp11 = __tmp2['recipient_id']
        __tmp5 = __tmp2['topic_name']
        tups.add((__tmp11, __tmp5.lower()))

    def __tmp3(__tmp11: int, topic: str) -> bool:
        return (__tmp11, topic.lower()) in tups

    return __tmp3
