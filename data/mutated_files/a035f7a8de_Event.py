from typing import TypeAlias
__typ1 : TypeAlias = "Rule"
__typ2 : TypeAlias = "BucketPoint"
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
__typ3 = Dict[BucketName, BucketType]
BucketPoints = List[__typ2]
BucketPointCondition = Callable[[__typ2], bool]


class EventsAnalyzer:
    browser_buckets_cache: Dict[BucketName, str] = {}

    def __init__(self) :
        self.matches_cache: Dict[str, Tuple[str, str]] = {}

    def analyze_events(self, buckets,
                       bucket_events) :
        __tmp0 = {}
        for bucket_name, bucket_type in buckets.items():
            events = bucket_events[bucket_name]
            __tmp0[bucket_name] = Timeline.create_from_bucket_events(
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
        browser_matches = self._match_browser_buckets(
            app_bucket,
            browser_buckets,
            __tmp0
        )
        for bucket_name in browser_buckets:
            if bucket_name not in browser_matches:
                del __tmp0[bucket_name]

        # leave only windows non-afk events
        __tmp0[app_bucket].intersect(
            __tmp0[afk_bucket],
            self.app_afk_timeline_condition
        )
        all_events: __typ0 = []
        # leave only web-events belonging to the corresponding app
        # (already non-afk)
        for web_bucket_name, app_name in browser_matches.items():
            __tmp0[web_bucket_name].intersect(
                __tmp0[app_bucket],
                self.app_browser_timeline_condition(app_name)
            )
            __tmp0[app_bucket].intersect(
                __tmp0[web_bucket_name],
                lambda _: True,
                False
            )
            all_events += __tmp0[web_bucket_name].get_events()

        all_events += __tmp0[app_bucket].get_events()
        all_events.sort()

        return all_events

    def match(self, events, projects) :
        matched_events = []
        for event in events:
            data_hash = event.stringify_data()
            if data_hash in self.matches_cache:
                hit = self.matches_cache[data_hash]
                matched_event = MatchedEvent(hit[0], hit[1], event)
            else:
                matched_event = self._match_event(event, projects)
                self.matches_cache[data_hash] = (matched_event.project,
                                                 matched_event.rule_id)
            matched_events.append(matched_event)

        return matched_events

    def _match_event(self, event, projects: Projects) -> MatchedEvent:
        for project in projects:
            for rule in project.rules:
                if self._is_event_matching(event, rule):
                    return MatchedEvent(project.name, rule.id, event)
        return MatchedEvent(projects.none_project, projects.none_project,
                            event)

    def _is_event_matching(self, event: <FILL>, definition) :
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
    def app_afk_timeline_condition(afk_event) -> bool:
        return bool(afk_event.event_data['status'] == 'not-afk')

    @staticmethod
    def app_browser_timeline_condition(app_name) :
        return lambda app_event: bool(app_event.event_data['app'] == app_name)

    @staticmethod
    def _match_browser_buckets(
            app_bucket: str,
            browser_buckets,
            __tmp0
    ) :
        app_timeline = __tmp0[app_bucket]
        matches = {}
        cache = EventsAnalyzer.browser_buckets_cache
        for browser_bucket in browser_buckets:
            if browser_bucket in cache:
                matches[browser_bucket] = cache[browser_bucket]
                continue

            browser_timeline = __tmp0[browser_bucket]
            match_app = browser_timeline.get_browser_app(app_timeline)

            if match_app is not None:
                matches[browser_bucket] = match_app
        return matches
