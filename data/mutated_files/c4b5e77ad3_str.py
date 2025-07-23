from typing import TypeAlias
__typ1 : TypeAlias = "Rule"
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "BucketPoint"
import re
from typing import Dict, List, Any, Callable, Tuple
from analyze.bucket_type import BucketType
from .event import Event
from .matched_event import MatchedEvent
from .bucket_point import BucketPoint
from .timeline import Timeline
from config import Rule, Projects

ClientBuckets = Dict[str, Dict[str, Any]]
__typ0 = List[Event]
BucketName = str
Buckets = Dict[BucketName, BucketType]
BucketPoints = List[__typ3]
BucketPointCondition = Callable[[__typ3], __typ2]


class EventsAnalyzer:
    browser_buckets_cache: Dict[BucketName, str] = {}

    def __tmp8(__tmp1) :
        __tmp1.matches_cache: Dict[str, Tuple[str, str]] = {}

    def __tmp9(__tmp1, __tmp0,
                       __tmp2) -> __typ0:
        __tmp4 = {}
        for bucket_name, bucket_type in __tmp0.items():
            __tmp11 = __tmp2[bucket_name]
            __tmp4[bucket_name] = Timeline.create_from_bucket_events(
                bucket_type,
                __tmp11
            )

        browser_buckets = [bucket
                           for bucket, value
                           in __tmp0.items()
                           if value == BucketType.WEB]
        app_buckets = [bucket
                       for bucket, value
                       in __tmp0.items()
                       if value == BucketType.APP]
        afk_buckets = [bucket
                       for bucket, value
                       in __tmp0.items()
                       if value == BucketType.AFK]

        if len(app_buckets) == 0 or len(afk_buckets) == 0:
            return []
        __tmp3 = app_buckets[0]
        afk_bucket = afk_buckets[0]
        browser_matches = __tmp1._match_browser_buckets(
            __tmp3,
            browser_buckets,
            __tmp4
        )
        for bucket_name in browser_buckets:
            if bucket_name not in browser_matches:
                del __tmp4[bucket_name]

        # leave only windows non-afk events
        __tmp4[__tmp3].intersect(
            __tmp4[afk_bucket],
            __tmp1.app_afk_timeline_condition
        )
        all_events: __typ0 = []
        # leave only web-events belonging to the corresponding app
        # (already non-afk)
        for web_bucket_name, __tmp10 in browser_matches.items():
            __tmp4[web_bucket_name].intersect(
                __tmp4[__tmp3],
                __tmp1.app_browser_timeline_condition(__tmp10)
            )
            __tmp4[__tmp3].intersect(
                __tmp4[web_bucket_name],
                lambda _: True,
                False
            )
            all_events += __tmp4[web_bucket_name].get_events()

        all_events += __tmp4[__tmp3].get_events()
        all_events.sort()

        return all_events

    def match(__tmp1, __tmp11: __typ0, __tmp7) :
        matched_events = []
        for event in __tmp11:
            data_hash = event.stringify_data()
            if data_hash in __tmp1.matches_cache:
                hit = __tmp1.matches_cache[data_hash]
                matched_event = MatchedEvent(hit[0], hit[1], event)
            else:
                matched_event = __tmp1._match_event(event, __tmp7)
                __tmp1.matches_cache[data_hash] = (matched_event.project,
                                                 matched_event.rule_id)
            matched_events.append(matched_event)

        return matched_events

    def _match_event(__tmp1, event, __tmp7) :
        for project in __tmp7:
            for rule in project.rules:
                if __tmp1._is_event_matching(event, rule):
                    return MatchedEvent(project.name, rule.id, event)
        return MatchedEvent(__tmp7.none_project, __tmp7.none_project,
                            event)

    def _is_event_matching(__tmp1, event, __tmp5) :
        if 'url' in __tmp5 and 'url' in event.data:
            return re.search(__tmp5['url'], event.data['url'],
                             flags=re.IGNORECASE) is not None
        if 'title' in __tmp5 and 'title' in event.data:
            return re.search(__tmp5['title'], event.data['title'],
                             flags=re.IGNORECASE) is not None
        if 'app' in __tmp5 and 'app' in event.data:
            return re.search(__tmp5['app'], event.data['app'],
                             flags=re.IGNORECASE) is not None
        return False

    @staticmethod
    def app_afk_timeline_condition(__tmp6) :
        return __typ2(__tmp6.event_data['status'] == 'not-afk')

    @staticmethod
    def app_browser_timeline_condition(__tmp10: <FILL>) -> BucketPointCondition:
        return lambda app_event: __typ2(app_event.event_data['app'] == __tmp10)

    @staticmethod
    def _match_browser_buckets(
            __tmp3: str,
            browser_buckets: List[BucketName],
            __tmp4
    ) :
        app_timeline = __tmp4[__tmp3]
        matches = {}
        cache = EventsAnalyzer.browser_buckets_cache
        for browser_bucket in browser_buckets:
            if browser_bucket in cache:
                matches[browser_bucket] = cache[browser_bucket]
                continue

            browser_timeline = __tmp4[browser_bucket]
            match_app = browser_timeline.get_browser_app(app_timeline)

            if match_app is not None:
                matches[browser_bucket] = match_app
        return matches
