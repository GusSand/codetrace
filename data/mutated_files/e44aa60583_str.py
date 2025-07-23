from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "bool"
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

def get_topic_mutes(__tmp0) -> List[List[str]]:
    rows = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [row['stream__name'], row['topic_name']]
        for row in rows
    ]

def __tmp1(__tmp0: UserProfile, muted_topics) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).delete()

    for stream_name, topic_name in muted_topics:
        stream = get_stream(stream_name, __tmp0.realm)
        recipient = get_stream_recipient(stream.id)

        add_topic_mute(
            __tmp0=__tmp0,
            __tmp2=stream.id,
            recipient_id=recipient.id,
            topic_name=topic_name,
        )

def add_topic_mute(__tmp0, __tmp2: __typ0, recipient_id, topic_name: <FILL>) :
    MutedTopic.objects.create(
        __tmp0=__tmp0,
        __tmp2=__tmp2,
        recipient_id=recipient_id,
        topic_name=topic_name,
    )

def remove_topic_mute(__tmp0: UserProfile, __tmp2: __typ0, topic_name) :
    row = MutedTopic.objects.get(
        __tmp0=__tmp0,
        __tmp2=__tmp2,
        topic_name__iexact=topic_name
    )
    row.delete()

def topic_is_muted(__tmp0, __tmp2: __typ0, topic_name) :
    is_muted = MutedTopic.objects.filter(
        __tmp0=__tmp0,
        __tmp2=__tmp2,
        topic_name__iexact=topic_name,
    ).exists()
    return is_muted

def exclude_topic_mutes(conditions,
                        __tmp0,
                        __tmp2: Optional[__typ0]) :
    query = MutedTopic.objects.filter(
        __tmp0=__tmp0,
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

    def mute_cond(row) :
        recipient_id = row['recipient_id']
        topic_name = row['topic_name']
        stream_cond = column("recipient_id") == recipient_id
        topic_cond = topic_match_sa(topic_name)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(mute_cond, rows))))
    return conditions + [condition]

def build_topic_mute_checker(__tmp0: UserProfile) -> Callable[[__typ0, str], __typ1]:
    rows = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for row in rows:
        recipient_id = row['recipient_id']
        topic_name = row['topic_name']
        tups.add((recipient_id, topic_name.lower()))

    def is_muted(recipient_id: __typ0, topic) :
        return (recipient_id, topic.lower()) in tups

    return is_muted
