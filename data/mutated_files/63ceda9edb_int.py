from typing import TypeAlias
__typ0 : TypeAlias = "Selectable"
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "UserProfile"
__typ3 : TypeAlias = "bool"
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

def __tmp0(__tmp1: __typ2) -> List[List[__typ1]]:
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp3['stream__name'], __tmp3['topic_name']]
        for __tmp3 in rows
    ]

def set_topic_mutes(__tmp1: __typ2, muted_topics: List[List[__typ1]]) -> None:

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).delete()

    for stream_name, __tmp4 in muted_topics:
        stream = get_stream(stream_name, __tmp1.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp7(
            __tmp1=__tmp1,
            __tmp2=stream.id,
            __tmp8=recipient.id,
            __tmp4=__tmp4,
        )

def __tmp7(__tmp1: __typ2, __tmp2, __tmp8, __tmp4: __typ1) :
    MutedTopic.objects.create(
        __tmp1=__tmp1,
        __tmp2=__tmp2,
        __tmp8=__tmp8,
        __tmp4=__tmp4,
    )

def __tmp5(__tmp1: __typ2, __tmp2: int, __tmp4) -> None:
    __tmp3 = MutedTopic.objects.get(
        __tmp1=__tmp1,
        __tmp2=__tmp2,
        topic_name__iexact=__tmp4
    )
    __tmp3.delete()

def topic_is_muted(__tmp1: __typ2, __tmp2, __tmp4: __typ1) -> __typ3:
    is_muted = MutedTopic.objects.filter(
        __tmp1=__tmp1,
        __tmp2=__tmp2,
        topic_name__iexact=__tmp4,
    ).exists()
    return is_muted

def exclude_topic_mutes(conditions: List[__typ0],
                        __tmp1: __typ2,
                        __tmp2) -> List[__typ0]:
    query = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    )

    if __tmp2 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp2=__tmp2)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return conditions

    def mute_cond(__tmp3: Dict[__typ1, Any]) -> __typ0:
        __tmp8 = __tmp3['recipient_id']
        __tmp4 = __tmp3['topic_name']
        stream_cond = column("recipient_id") == __tmp8
        topic_cond = topic_match_sa(__tmp4)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(mute_cond, rows))))
    return conditions + [condition]

def __tmp6(__tmp1: __typ2) :
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp3 in rows:
        __tmp8 = __tmp3['recipient_id']
        __tmp4 = __tmp3['topic_name']
        tups.add((__tmp8, __tmp4.lower()))

    def is_muted(__tmp8: <FILL>, topic: __typ1) -> __typ3:
        return (__tmp8, topic.lower()) in tups

    return is_muted
