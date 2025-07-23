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

def get_topic_mutes(user_profile) :
    rows = MutedTopic.objects.filter(
        user_profile=user_profile,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [row['stream__name'], row['topic_name']]
        for row in rows
    ]

def __tmp0(user_profile, muted_topics: List[List[__typ0]]) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        user_profile=user_profile,
    ).delete()

    for stream_name, topic_name in muted_topics:
        stream = get_stream(stream_name, user_profile.realm)
        recipient = get_stream_recipient(stream.id)

        add_topic_mute(
            user_profile=user_profile,
            stream_id=stream.id,
            recipient_id=recipient.id,
            topic_name=topic_name,
        )

def add_topic_mute(user_profile, stream_id: __typ2, recipient_id: __typ2, topic_name) :
    MutedTopic.objects.create(
        user_profile=user_profile,
        stream_id=stream_id,
        recipient_id=recipient_id,
        topic_name=topic_name,
    )

def remove_topic_mute(user_profile, stream_id, topic_name: __typ0) -> None:
    row = MutedTopic.objects.get(
        user_profile=user_profile,
        stream_id=stream_id,
        topic_name__iexact=topic_name
    )
    row.delete()

def topic_is_muted(user_profile, stream_id, topic_name: __typ0) -> __typ3:
    is_muted = MutedTopic.objects.filter(
        user_profile=user_profile,
        stream_id=stream_id,
        topic_name__iexact=topic_name,
    ).exists()
    return is_muted

def exclude_topic_mutes(conditions,
                        user_profile: <FILL>,
                        stream_id: Optional[__typ2]) :
    query = MutedTopic.objects.filter(
        user_profile=user_profile,
    )

    if stream_id is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(stream_id=stream_id)

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

def build_topic_mute_checker(user_profile) -> Callable[[__typ2, __typ0], __typ3]:
    rows = MutedTopic.objects.filter(
        user_profile=user_profile,
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

    def is_muted(recipient_id, topic) :
        return (recipient_id, topic.lower()) in tups

    return is_muted
