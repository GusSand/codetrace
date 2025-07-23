from datetime import datetime, timezone
from typing import Dict, Any, List
from analyze.bucket_type import BucketType
from .event import Event
from aw_client import ActivityWatchClient


Events = List[Event]
__typ0 = Dict[str, BucketType]


class EventRepository:
    BUCKET_TYPE_WINDOW = 'currentwindow'
    BUCKET_TYPE_AFK = 'afkstatus'
    BUCKET_TYPE_WEB = 'web.tab.current'

    def __tmp2(__tmp1, client: ActivityWatchClient) :
        __tmp1.client = client

    def fetch_buckets(__tmp1) :
        return {
            key: __tmp1._get_bucket_type(value)
            for key, value
            in __tmp1.client.get_buckets().items()
            if value['type'] in [
                EventRepository.BUCKET_TYPE_WINDOW,
                EventRepository.BUCKET_TYPE_AFK,
                EventRepository.BUCKET_TYPE_WEB,
            ]
        }

    def _get_bucket_type(__tmp1, data) -> BucketType:
        if data['type'] == EventRepository.BUCKET_TYPE_AFK:
            return BucketType.AFK
        elif data['type'] == EventRepository.BUCKET_TYPE_WINDOW:
            return BucketType.APP
        elif data['type'] == EventRepository.BUCKET_TYPE_WEB:
            return BucketType.WEB
        else:
            raise RuntimeError

    def get_events(__tmp1, bucket: str, __tmp3: datetime,
                   __tmp4) :
        events = __tmp1.client.get_events(bucket, -1,
                                        __tmp3.astimezone(timezone.utc),
                                        __tmp4.astimezone(timezone.utc))
        bucket_type = __tmp1.fetch_buckets()[bucket]
        return [Event(event, bucket_type)
                for event
                in events
                if event.duration.total_seconds() > 0]

    def get_bucket_events(__tmp1, __tmp0: List[str], __tmp3: <FILL>,
                          __tmp4) -> Dict[str, Events]:
        events = {}
        for bucket_name in __tmp0:
            events[bucket_name] = __tmp1.get_events(
                bucket_name,
                __tmp3,
                __tmp4
            )

        return events
