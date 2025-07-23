from typing import TypeAlias
__typ3 : TypeAlias = "Event"
__typ4 : TypeAlias = "BucketPoint"
__typ2 : TypeAlias = "MatchedEvent"
__typ1 : TypeAlias = "str"
import re
from typing import Dict, List, Any, Callable, Tuple
from analyze.bucket_type import BucketType
from .event import Event
from .matched_event import MatchedEvent
from .bucket_point import BucketPoint
from .timeline import Timeline
from config import Rule, Projects

ClientBuckets = Dict[__typ1, Dict[__typ1, Any]]
Events = List[__typ3]
BucketName = __typ1
__typ0 = Dict[BucketName, BucketType]
BucketPoints = List[__typ4]
BucketPointCondition = Callable[[__typ4], bool]


class EventsAnalyzer:
    browser_buckets_cache: Dict[BucketName, __typ1] = {}

    def __tmp4(__tmp0) -> None:
        __tmp0.matches_cache: Dict[__typ1, Tuple[__typ1, __typ1]] = {}

    def __tmp5(__tmp0, buckets: __typ0,
                       __tmp1: Dict[BucketName, Events]) -> Events:
        timelines = {}
        for bucket_name, bucket_type in buckets.items():
            __tmp6 = __tmp1[bucket_name]
            timelines[bucket_name] = Timeline.create_from_bucket_events(
                bucket_type,
                __tmp6
            )

        __tmp7 = [bucket
                           for bucket, value
                           in buckets.items()
                           if value == BucketType.WEB]
        app_buckets = [bucket
                       for bucket, value
                       in buckets.items()
                       if value == BucketType.APP]
        afk_buckets = [bucket
                       for bucket, value
                       in buckets.items()
                       if value == BucketType.AFK]

        if len(app_buckets) == 0 or len(afk_buckets) == 0:
            return []
        app_bucket = app_buckets[0]
        afk_bucket = afk_buckets[0]
        browser_matches = __tmp0._match_browser_buckets(
            app_bucket,
            __tmp7,
            timelines
        )
        for bucket_name in __tmp7:
            if bucket_name not in browser_matches:
                del timelines[bucket_name]

        # leave only windows non-afk events
        timelines[app_bucket].intersect(
            timelines[afk_bucket],
            __tmp0.app_afk_timeline_condition
        )
        all_events: Events = []
        # leave only web-events belonging to the corresponding app
        # (already non-afk)
        for web_bucket_name, app_name in browser_matches.items():
            timelines[web_bucket_name].intersect(
                timelines[app_bucket],
                __tmp0.app_browser_timeline_condition(app_name)
            )
            timelines[app_bucket].intersect(
                timelines[web_bucket_name],
                lambda _: True,
                False
            )
            all_events += timelines[web_bucket_name].get_events()

        all_events += timelines[app_bucket].get_events()
        all_events.sort()

        return all_events

    def match(__tmp0, __tmp6: Events, __tmp3: Projects) -> List[__typ2]:
        matched_events = []
        for event in __tmp6:
            data_hash = event.stringify_data()
            if data_hash in __tmp0.matches_cache:
                hit = __tmp0.matches_cache[data_hash]
                matched_event = __typ2(hit[0], hit[1], event)
            else:
                matched_event = __tmp0._match_event(event, __tmp3)
                __tmp0.matches_cache[data_hash] = (matched_event.project,
                                                 matched_event.rule_id)
            matched_events.append(matched_event)

        return matched_events

    def _match_event(__tmp0, event: __typ3, __tmp3: <FILL>) :
        for project in __tmp3:
            for rule in project.rules:
                if __tmp0._is_event_matching(event, rule):
                    return __typ2(project.name, rule.id, event)
        return __typ2(__tmp3.none_project, __tmp3.none_project,
                            event)

    def _is_event_matching(__tmp0, event, __tmp2: Rule) -> bool:
        if 'url' in __tmp2 and 'url' in event.data:
            return re.search(__tmp2['url'], event.data['url'],
                             flags=re.IGNORECASE) is not None
        if 'title' in __tmp2 and 'title' in event.data:
            return re.search(__tmp2['title'], event.data['title'],
                             flags=re.IGNORECASE) is not None
        if 'app' in __tmp2 and 'app' in event.data:
            return re.search(__tmp2['app'], event.data['app'],
                             flags=re.IGNORECASE) is not None
        return False

    @staticmethod
    def app_afk_timeline_condition(afk_event: __typ4) -> bool:
        return bool(afk_event.event_data['status'] == 'not-afk')

    @staticmethod
    def app_browser_timeline_condition(app_name: __typ1) -> BucketPointCondition:
        return lambda app_event: bool(app_event.event_data['app'] == app_name)

    @staticmethod
    def _match_browser_buckets(
            app_bucket,
            __tmp7: List[BucketName],
            timelines: Dict[BucketName, Timeline]
    ) -> Dict[BucketName, __typ1]:
        app_timeline = timelines[app_bucket]
        matches = {}
        cache = EventsAnalyzer.browser_buckets_cache
        for browser_bucket in __tmp7:
            if browser_bucket in cache:
                matches[browser_bucket] = cache[browser_bucket]
                continue

            browser_timeline = timelines[browser_bucket]
            match_app = browser_timeline.get_browser_app(app_timeline)

            if match_app is not None:
                matches[browser_bucket] = match_app
        return matches
