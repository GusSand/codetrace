from typing import TypeAlias
__typ1 : TypeAlias = "BucketPoint"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
import re
from typing import Dict, List, Any, Callable, Tuple
from analyze.bucket_type import BucketType
from .event import Event
from .matched_event import MatchedEvent
from .bucket_point import BucketPoint
from .timeline import Timeline
from config import Rule, Projects

ClientBuckets = Dict[__typ0, Dict[__typ0, Any]]
Events = List[Event]
BucketName = __typ0
Buckets = Dict[BucketName, BucketType]
BucketPoints = List[__typ1]
BucketPointCondition = Callable[[__typ1], __typ2]


class EventsAnalyzer:
    browser_buckets_cache: Dict[BucketName, __typ0] = {}

    def __tmp3(__tmp0) -> None:
        __tmp0.matches_cache: Dict[__typ0, Tuple[__typ0, __typ0]] = {}

    def __tmp4(__tmp0, buckets: <FILL>,
                       __tmp1: Dict[BucketName, Events]) -> Events:
        timelines = {}
        for bucket_name, bucket_type in buckets.items():
            events = __tmp1[bucket_name]
            timelines[bucket_name] = Timeline.create_from_bucket_events(
                bucket_type,
                events
            )

        browser_buckets = [bucket
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
            browser_buckets,
            timelines
        )
        for bucket_name in browser_buckets:
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
        for web_bucket_name, __tmp5 in browser_matches.items():
            timelines[web_bucket_name].intersect(
                timelines[app_bucket],
                __tmp0.app_browser_timeline_condition(__tmp5)
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

    def match(__tmp0, events, projects: Projects) -> List[MatchedEvent]:
        matched_events = []
        for event in events:
            data_hash = event.stringify_data()
            if data_hash in __tmp0.matches_cache:
                hit = __tmp0.matches_cache[data_hash]
                matched_event = MatchedEvent(hit[0], hit[1], event)
            else:
                matched_event = __tmp0._match_event(event, projects)
                __tmp0.matches_cache[data_hash] = (matched_event.project,
                                                 matched_event.rule_id)
            matched_events.append(matched_event)

        return matched_events

    def _match_event(__tmp0, event: Event, projects) -> MatchedEvent:
        for project in projects:
            for rule in project.rules:
                if __tmp0._is_event_matching(event, rule):
                    return MatchedEvent(project.name, rule.id, event)
        return MatchedEvent(projects.none_project, projects.none_project,
                            event)

    def _is_event_matching(__tmp0, event: Event, definition: Rule) -> __typ2:
        if 'url' in definition and 'url' in event.data:
            return re.search(definition['url'], event.data['url'],
                             flags=re.IGNORECASE) is not None
        if 'title' in definition and 'title' in event.data:
            return re.search(definition['title'], event.data['title'],
                             flags=re.IGNORECASE) is not None
        if 'app' in definition and 'app' in event.data:
            return re.search(definition['app'], event.data['app'],
                             flags=re.IGNORECASE) is not None
        return False

    @staticmethod
    def app_afk_timeline_condition(__tmp2: __typ1) -> __typ2:
        return __typ2(__tmp2.event_data['status'] == 'not-afk')

    @staticmethod
    def app_browser_timeline_condition(__tmp5: __typ0) -> BucketPointCondition:
        return lambda app_event: __typ2(app_event.event_data['app'] == __tmp5)

    @staticmethod
    def _match_browser_buckets(
            app_bucket: __typ0,
            browser_buckets: List[BucketName],
            timelines: Dict[BucketName, Timeline]
    ) -> Dict[BucketName, __typ0]:
        app_timeline = timelines[app_bucket]
        matches = {}
        cache = EventsAnalyzer.browser_buckets_cache
        for browser_bucket in browser_buckets:
            if browser_bucket in cache:
                matches[browser_bucket] = cache[browser_bucket]
                continue

            browser_timeline = timelines[browser_bucket]
            match_app = browser_timeline.get_browser_app(app_timeline)

            if match_app is not None:
                matches[browser_bucket] = match_app
        return matches
