from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "str"
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

def __tmp1(__tmp2: __typ1) -> List[List[__typ0]]:
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp4['stream__name'], __tmp4['topic_name']]
        for __tmp4 in rows
    ]

def __tmp5(__tmp2, muted_topics) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).delete()

    for stream_name, __tmp7 in muted_topics:
        stream = get_stream(stream_name, __tmp2.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp11(
            __tmp2=__tmp2,
            __tmp3=stream.id,
            __tmp12=recipient.id,
            __tmp7=__tmp7,
        )

def __tmp11(__tmp2: __typ1, __tmp3, __tmp12, __tmp7) -> None:
    MutedTopic.objects.create(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        __tmp12=__tmp12,
        __tmp7=__tmp7,
    )

def remove_topic_mute(__tmp2: __typ1, __tmp3: <FILL>, __tmp7: __typ0) :
    __tmp4 = MutedTopic.objects.get(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp7
    )
    __tmp4.delete()

def __tmp9(__tmp2, __tmp3: int, __tmp7) :
    is_muted = MutedTopic.objects.filter(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp7,
    ).exists()
    return is_muted

def __tmp8(__tmp10: List[Selectable],
                        __tmp2,
                        __tmp3: Optional[int]) :
    query = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    )

    if __tmp3 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp3=__tmp3)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return __tmp10

    def __tmp0(__tmp4: Dict[__typ0, Any]) :
        __tmp12 = __tmp4['recipient_id']
        __tmp7 = __tmp4['topic_name']
        stream_cond = column("recipient_id") == __tmp12
        topic_cond = topic_match_sa(__tmp7)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return __tmp10 + [condition]

def __tmp6(__tmp2: __typ1) :
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp4 in rows:
        __tmp12 = __tmp4['recipient_id']
        __tmp7 = __tmp4['topic_name']
        tups.add((__tmp12, __tmp7.lower()))

    def is_muted(__tmp12, topic: __typ0) -> bool:
        return (__tmp12, topic.lower()) in tups

    return is_muted
