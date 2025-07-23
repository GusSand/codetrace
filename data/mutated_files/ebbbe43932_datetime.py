from datetime import datetime, timezone
from typing import Dict, Any, List
from analyze.bucket_type import BucketType
from .event import Event
from aw_client import ActivityWatchClient


Events = List[Event]
Buckets = Dict[str, BucketType]


class __typ0:
    BUCKET_TYPE_WINDOW = 'currentwindow'
    BUCKET_TYPE_AFK = 'afkstatus'
    BUCKET_TYPE_WEB = 'web.tab.current'

    def __tmp1(__tmp0, client) :
        __tmp0.client = client

    def fetch_buckets(__tmp0) :
        return {
            key: __tmp0._get_bucket_type(value)
            for key, value
            in __tmp0.client.get_buckets().items()
            if value['type'] in [
                __typ0.BUCKET_TYPE_WINDOW,
                __typ0.BUCKET_TYPE_AFK,
                __typ0.BUCKET_TYPE_WEB,
            ]
        }

    def _get_bucket_type(__tmp0, __tmp2) :
        if __tmp2['type'] == __typ0.BUCKET_TYPE_AFK:
            return BucketType.AFK
        elif __tmp2['type'] == __typ0.BUCKET_TYPE_WINDOW:
            return BucketType.APP
        elif __tmp2['type'] == __typ0.BUCKET_TYPE_WEB:
            return BucketType.WEB
        else:
            raise RuntimeError

    def get_events(__tmp0, bucket, start_date,
                   end_date: <FILL>) -> Events:
        events = __tmp0.client.get_events(bucket, -1,
                                        start_date.astimezone(timezone.utc),
                                        end_date.astimezone(timezone.utc))
        bucket_type = __tmp0.fetch_buckets()[bucket]
        return [Event(event, bucket_type)
                for event
                in events
                if event.duration.total_seconds() > 0]

    def get_bucket_events(__tmp0, buckets, start_date,
                          end_date: datetime) -> Dict[str, Events]:
        events = {}
        for bucket_name in buckets:
            events[bucket_name] = __tmp0.get_events(
                bucket_name,
                start_date,
                end_date
            )

        return events
