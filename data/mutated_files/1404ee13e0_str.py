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

def __tmp0(__tmp1) :
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp4['stream__name'], __tmp4['topic_name']]
        for __tmp4 in rows
    ]

def __tmp6(__tmp1: __typ0, muted_topics: List[List[str]]) -> None:

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).delete()

    for stream_name, topic_name in muted_topics:
        stream = get_stream(stream_name, __tmp1.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp8(
            __tmp1=__tmp1,
            __tmp3=stream.id,
            recipient_id=recipient.id,
            topic_name=topic_name,
        )

def __tmp8(__tmp1: __typ0, __tmp3, recipient_id, topic_name: str) -> None:
    MutedTopic.objects.create(
        __tmp1=__tmp1,
        __tmp3=__tmp3,
        recipient_id=recipient_id,
        topic_name=topic_name,
    )

def remove_topic_mute(__tmp1, __tmp3: int, topic_name: str) :
    __tmp4 = MutedTopic.objects.get(
        __tmp1=__tmp1,
        __tmp3=__tmp3,
        topic_name__iexact=topic_name
    )
    __tmp4.delete()

def topic_is_muted(__tmp1: __typ0, __tmp3, topic_name: <FILL>) :
    __tmp2 = MutedTopic.objects.filter(
        __tmp1=__tmp1,
        __tmp3=__tmp3,
        topic_name__iexact=topic_name,
    ).exists()
    return __tmp2

def exclude_topic_mutes(__tmp7: List[Selectable],
                        __tmp1,
                        __tmp3) :
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
        return __tmp7

    def mute_cond(__tmp4) :
        recipient_id = __tmp4['recipient_id']
        topic_name = __tmp4['topic_name']
        stream_cond = column("recipient_id") == recipient_id
        topic_cond = topic_match_sa(topic_name)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(mute_cond, rows))))
    return __tmp7 + [condition]

def __tmp5(__tmp1) :
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp4 in rows:
        recipient_id = __tmp4['recipient_id']
        topic_name = __tmp4['topic_name']
        tups.add((recipient_id, topic_name.lower()))

    def __tmp2(recipient_id, topic) :
        return (recipient_id, topic.lower()) in tups

    return __tmp2
