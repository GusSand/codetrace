from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
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

def __tmp1(__tmp2) :
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [row['stream__name'], row['topic_name']]
        for row in rows
    ]

def __tmp5(__tmp2, __tmp8: List[List[str]]) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).delete()

    for stream_name, __tmp7 in __tmp8:
        stream = get_stream(stream_name, __tmp2.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp12(
            __tmp2=__tmp2,
            __tmp3=stream.id,
            __tmp13=recipient.id,
            __tmp7=__tmp7,
        )

def __tmp12(__tmp2: __typ0, __tmp3: int, __tmp13: int, __tmp7: str) -> None:
    MutedTopic.objects.create(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        __tmp13=__tmp13,
        __tmp7=__tmp7,
    )

def __tmp10(__tmp2: __typ0, __tmp3, __tmp7: str) :
    row = MutedTopic.objects.get(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp7
    )
    row.delete()

def topic_is_muted(__tmp2, __tmp3: <FILL>, __tmp7: str) -> bool:
    __tmp4 = MutedTopic.objects.filter(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp7,
    ).exists()
    return __tmp4

def __tmp9(__tmp11: List[Selectable],
                        __tmp2: __typ0,
                        __tmp3: Optional[int]) -> List[Selectable]:
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
        return __tmp11

    def __tmp0(row: Dict[str, Any]) :
        __tmp13 = row['recipient_id']
        __tmp7 = row['topic_name']
        stream_cond = column("recipient_id") == __tmp13
        topic_cond = topic_match_sa(__tmp7)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return __tmp11 + [condition]

def __tmp6(__tmp2: __typ0) :
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for row in rows:
        __tmp13 = row['recipient_id']
        __tmp7 = row['topic_name']
        tups.add((__tmp13, __tmp7.lower()))

    def __tmp4(__tmp13: int, topic: str) -> bool:
        return (__tmp13, topic.lower()) in tups

    return __tmp4
