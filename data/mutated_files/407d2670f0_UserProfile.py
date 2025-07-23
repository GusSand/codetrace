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

def __tmp1(__tmp2) :
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

def set_topic_mutes(__tmp2: UserProfile, __tmp6) -> None:

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).delete()

    for stream_name, __tmp5 in __tmp6:
        stream = get_stream(stream_name, __tmp2.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp8(
            __tmp2=__tmp2,
            __tmp3=stream.id,
            recipient_id=recipient.id,
            __tmp5=__tmp5,
        )

def __tmp8(__tmp2, __tmp3: __typ2, recipient_id: __typ2, __tmp5: __typ0) :
    MutedTopic.objects.create(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        recipient_id=recipient_id,
        __tmp5=__tmp5,
    )

def remove_topic_mute(__tmp2: UserProfile, __tmp3, __tmp5) :
    __tmp4 = MutedTopic.objects.get(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp5
    )
    __tmp4.delete()

def topic_is_muted(__tmp2: <FILL>, __tmp3, __tmp5: __typ0) -> __typ3:
    is_muted = MutedTopic.objects.filter(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp5,
    ).exists()
    return is_muted

def exclude_topic_mutes(conditions,
                        __tmp2: UserProfile,
                        __tmp3) -> List[__typ1]:
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
        return conditions

    def __tmp0(__tmp4) :
        recipient_id = __tmp4['recipient_id']
        __tmp5 = __tmp4['topic_name']
        stream_cond = column("recipient_id") == recipient_id
        topic_cond = topic_match_sa(__tmp5)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return conditions + [condition]

def __tmp7(__tmp2: UserProfile) -> Callable[[__typ2, __typ0], __typ3]:
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp4 in rows:
        recipient_id = __tmp4['recipient_id']
        __tmp5 = __tmp4['topic_name']
        tups.add((recipient_id, __tmp5.lower()))

    def is_muted(recipient_id: __typ2, topic: __typ0) -> __typ3:
        return (recipient_id, topic.lower()) in tups

    return is_muted
