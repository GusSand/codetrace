from typing import TypeAlias
__typ1 : TypeAlias = "Rule"
__typ3 : TypeAlias = "str"
__typ4 : TypeAlias = "bool"
import re
from typing import Dict, List, Any, Callable, Tuple
from analyze.bucket_type import BucketType
from .event import Event
from .matched_event import MatchedEvent
from .bucket_point import BucketPoint
from .timeline import Timeline
from config import Rule, Projects

ClientBuckets = Dict[__typ3, Dict[__typ3, Any]]
Events = List[Event]
BucketName = __typ3
__typ2 = Dict[BucketName, BucketType]
BucketPoints = List[BucketPoint]
__typ0 = Callable[[BucketPoint], __typ4]


class EventsAnalyzer:
    browser_buckets_cache: Dict[BucketName, __typ3] = {}

    def __init__(__tmp0) -> None:
        __tmp0.matches_cache: Dict[__typ3, Tuple[__typ3, __typ3]] = {}

    def analyze_events(__tmp0, buckets,
                       bucket_events) :
        __tmp3 = {}
        for bucket_name, bucket_type in buckets.items():
            events = bucket_events[bucket_name]
            __tmp3[bucket_name] = Timeline.create_from_bucket_events(
                bucket_type,
                events
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
        __tmp1 = app_buckets[0]
        afk_bucket = afk_buckets[0]
        browser_matches = __tmp0._match_browser_buckets(
            __tmp1,
            __tmp7,
            __tmp3
        )
        for bucket_name in __tmp7:
            if bucket_name not in browser_matches:
                del __tmp3[bucket_name]

        # leave only windows non-afk events
        __tmp3[__tmp1].intersect(
            __tmp3[afk_bucket],
            __tmp0.app_afk_timeline_condition
        )
        all_events: Events = []
        # leave only web-events belonging to the corresponding app
        # (already non-afk)
        for web_bucket_name, __tmp6 in browser_matches.items():
            __tmp3[web_bucket_name].intersect(
                __tmp3[__tmp1],
                __tmp0.app_browser_timeline_condition(__tmp6)
            )
            __tmp3[__tmp1].intersect(
                __tmp3[web_bucket_name],
                lambda _: True,
                False
            )
            all_events += __tmp3[web_bucket_name].get_events()

        all_events += __tmp3[__tmp1].get_events()
        all_events.sort()

        return all_events

    def match(__tmp0, events, __tmp5: <FILL>) :
        matched_events = []
        for event in events:
            data_hash = event.stringify_data()
            if data_hash in __tmp0.matches_cache:
                hit = __tmp0.matches_cache[data_hash]
                matched_event = MatchedEvent(hit[0], hit[1], event)
            else:
                matched_event = __tmp0._match_event(event, __tmp5)
                __tmp0.matches_cache[data_hash] = (matched_event.project,
                                                 matched_event.rule_id)
            matched_events.append(matched_event)

        return matched_events

    def _match_event(__tmp0, event, __tmp5) :
        for project in __tmp5:
            for rule in project.rules:
                if __tmp0._is_event_matching(event, rule):
                    return MatchedEvent(project.name, rule.id, event)
        return MatchedEvent(__tmp5.none_project, __tmp5.none_project,
                            event)

    def _is_event_matching(__tmp0, event, __tmp2) -> __typ4:
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
    def app_afk_timeline_condition(__tmp4) :
        return __typ4(__tmp4.event_data['status'] == 'not-afk')

    @staticmethod
    def app_browser_timeline_condition(__tmp6) :
        return lambda app_event: __typ4(app_event.event_data['app'] == __tmp6)

    @staticmethod
    def _match_browser_buckets(
            __tmp1,
            __tmp7: List[BucketName],
            __tmp3: Dict[BucketName, Timeline]
    ) -> Dict[BucketName, __typ3]:
        app_timeline = __tmp3[__tmp1]
        matches = {}
        cache = EventsAnalyzer.browser_buckets_cache
        for browser_bucket in __tmp7:
            if browser_bucket in cache:
                matches[browser_bucket] = cache[browser_bucket]
                continue

            browser_timeline = __tmp3[browser_bucket]
            match_app = browser_timeline.get_browser_app(app_timeline)

            if match_app is not None:
                matches[browser_bucket] = match_app
        return matches
