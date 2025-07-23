from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
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

def __tmp1(__tmp2: <FILL>) :
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

def __tmp5(__tmp2, muted_topics) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).delete()

    for stream_name, __tmp6 in muted_topics:
        stream = get_stream(stream_name, __tmp2.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp9(
            __tmp2=__tmp2,
            __tmp4=stream.id,
            __tmp10=recipient.id,
            __tmp6=__tmp6,
        )

def __tmp9(__tmp2, __tmp4, __tmp10, __tmp6) :
    MutedTopic.objects.create(
        __tmp2=__tmp2,
        __tmp4=__tmp4,
        __tmp10=__tmp10,
        __tmp6=__tmp6,
    )

def remove_topic_mute(__tmp2: UserProfile, __tmp4: __typ0, __tmp6) :
    row = MutedTopic.objects.get(
        __tmp2=__tmp2,
        __tmp4=__tmp4,
        topic_name__iexact=__tmp6
    )
    row.delete()

def topic_is_muted(__tmp2, __tmp4, __tmp6) -> __typ2:
    __tmp3 = MutedTopic.objects.filter(
        __tmp2=__tmp2,
        __tmp4=__tmp4,
        topic_name__iexact=__tmp6,
    ).exists()
    return __tmp3

def __tmp7(__tmp8,
                        __tmp2,
                        __tmp4) :
    query = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    )

    if __tmp4 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp4=__tmp4)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return __tmp8

    def __tmp0(row: Dict[__typ1, Any]) -> Selectable:
        __tmp10 = row['recipient_id']
        __tmp6 = row['topic_name']
        stream_cond = column("recipient_id") == __tmp10
        topic_cond = topic_match_sa(__tmp6)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return __tmp8 + [condition]

def build_topic_mute_checker(__tmp2) :
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for row in rows:
        __tmp10 = row['recipient_id']
        __tmp6 = row['topic_name']
        tups.add((__tmp10, __tmp6.lower()))

    def __tmp3(__tmp10: __typ0, topic) :
        return (__tmp10, topic.lower()) in tups

    return __tmp3
