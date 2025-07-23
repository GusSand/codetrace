from typing import TypeAlias
__typ1 : TypeAlias = "Selectable"
__typ2 : TypeAlias = "int"
__typ0 : TypeAlias = "str"
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

def get_topic_mutes(__tmp1: UserProfile) :
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [row['stream__name'], row['topic_name']]
        for row in rows
    ]

def set_topic_mutes(__tmp1: <FILL>, __tmp5: List[List[__typ0]]) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).delete()

    for stream_name, __tmp4 in __tmp5:
        stream = get_stream(stream_name, __tmp1.realm)
        recipient = get_stream_recipient(stream.id)

        add_topic_mute(
            __tmp1=__tmp1,
            __tmp3=stream.id,
            __tmp10=recipient.id,
            __tmp4=__tmp4,
        )

def add_topic_mute(__tmp1: UserProfile, __tmp3: __typ2, __tmp10: __typ2, __tmp4: __typ0) :
    MutedTopic.objects.create(
        __tmp1=__tmp1,
        __tmp3=__tmp3,
        __tmp10=__tmp10,
        __tmp4=__tmp4,
    )

def __tmp8(__tmp1, __tmp3, __tmp4) :
    row = MutedTopic.objects.get(
        __tmp1=__tmp1,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp4
    )
    row.delete()

def __tmp7(__tmp1: UserProfile, __tmp3: __typ2, __tmp4: __typ0) :
    __tmp2 = MutedTopic.objects.filter(
        __tmp1=__tmp1,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp4,
    ).exists()
    return __tmp2

def __tmp6(__tmp9: List[__typ1],
                        __tmp1: UserProfile,
                        __tmp3: Optional[__typ2]) -> List[__typ1]:
    query = MutedTopic.objects.filter(
        __tmp1=__tmp1,
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
        return __tmp9

    def __tmp0(row: Dict[__typ0, Any]) :
        __tmp10 = row['recipient_id']
        __tmp4 = row['topic_name']
        stream_cond = column("recipient_id") == __tmp10
        topic_cond = topic_match_sa(__tmp4)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return __tmp9 + [condition]

def build_topic_mute_checker(__tmp1: UserProfile) -> Callable[[__typ2, __typ0], __typ3]:
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for row in rows:
        __tmp10 = row['recipient_id']
        __tmp4 = row['topic_name']
        tups.add((__tmp10, __tmp4.lower()))

    def __tmp2(__tmp10: __typ2, topic: __typ0) -> __typ3:
        return (__tmp10, topic.lower()) in tups

    return __tmp2
