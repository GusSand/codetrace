from typing import TypeAlias
__typ1 : TypeAlias = "BucketType"
__typ3 : TypeAlias = "bool"
import datetime
from typing import Callable, List, Optional, Dict
from aw_core import Event as ParentEvent
from .event import Event
from .bucket_point import BucketPoint
from .bucket_type import BucketType

Events = List[Event]
__typ2 = List[BucketPoint]


class Timeline:
    __typ0 = Callable[[BucketPoint], __typ3]

    @staticmethod
    def __tmp4(bucket_type,
                                  events: <FILL>
                                  ) -> 'Timeline':
        all_points = []
        for event in events:
            all_points.append(BucketPoint(bucket_type,
                                          event.timestamp,
                                          event,
                                          False))
            all_points.append(BucketPoint(
                bucket_type,
                event.timestamp + event.duration,
                event,
                True
            ))

        return Timeline(bucket_type, all_points)

    def __tmp3(__tmp1, bucket_type: __typ1, points):
        __tmp1._bucket_type = bucket_type
        __tmp1.points = points
        __tmp1.points.sort()

    def intersect(__tmp1, spec_timeline: 'Timeline',
                  __tmp0,
                  is_inclusive: __typ3 = True) :
        """
        Finds an intersection of 2 timelines.
        Replaces all points of the current timeline by those which intersect
        (or not if exclusively) the given timeline

        :param spec_timeline: Timeline to compare against
        :param intersect_condition: Conditional function which defines
            which points in spec_timeline are inside intersection
        :param is_inclusive: If False then those points are returned
            which don't belong to the intersection
        """
        points = __tmp1.points
        for point in spec_timeline.points:
            points.append(point)
        points.sort()

        cut_points = []
        is_exclusive = not is_inclusive
        # inclusive: inside intersection condition
        # exclusive: outside intersection condition
        in_intersection = is_exclusive
        opened_point = None
        for point in points:
            if spec_timeline._is_source_of_point(point):
                if not __tmp0(point):
                    continue

                if not point.is_end():
                    intersection_started = is_inclusive
                else:
                    intersection_started = is_exclusive
                intersection_ended = not intersection_started

                if opened_point is not None:
                    cut_points.append(BucketPoint(
                        opened_point.event_type,
                        point.timestamp,
                        opened_point.event,
                        intersection_ended
                    ))
                in_intersection = intersection_started
            else:
                if in_intersection:
                    cut_points.append(point)
                if not point.is_end():
                    opened_point = point
                else:
                    opened_point = None

        if len(cut_points) > 0:
            __tmp1._filter_empty_points(cut_points)

        __tmp1.points = cut_points

    def _is_source_of_point(__tmp1, point: BucketPoint) :
        # consider using generated timeline id
        return point.event_type == __tmp1._bucket_type

    def _filter_empty_points(__tmp1, cut_points) :
        current_time = cut_points[-1].timestamp
        close_points: Dict[int, BucketPoint] = {}
        for i in reversed(range(len(cut_points))):
            point = cut_points[i]
            if point.timestamp != current_time:
                close_points.clear()
                current_time = point.timestamp
            if point.is_end():
                close_points[i] = point
            elif len(close_points) > 0:
                for index, opened_point in close_points.items():
                    if point.event is opened_point.event:
                        del cut_points[index]
                        del cut_points[i]

    def get_browser_app(__tmp1, app_timeline: 'Timeline') -> Optional[str]:
        for point in __tmp1.points:
            app_point = app_timeline._get_event_at(point.timestamp)
            if app_point is None:
                continue
            app_point_title = app_point.event_data['title']
            point_title = point.event_data['title']
            if app_point_title.startswith(point_title):
                return str(app_point.event_data['app'])
        return None

    def _get_event_at(__tmp1,
                      at_time) :
        last_event = None
        for point in __tmp1.points:
            if point.is_end():
                continue
            if last_event is None:
                if point.timestamp > at_time:
                    # we don't know about the event
                    # before the 1st event in the timeline
                    return None
            elif at_time < point.timestamp:
                return last_event
            last_event = point
        return None

    def __tmp2(__tmp1) :
        events = []
        for open_i in range(len(__tmp1.points)):
            open_point = __tmp1.points[open_i]
            if open_point.is_end():
                continue
            for close_i in range(open_i + 1, len(__tmp1.points)):
                close_point = __tmp1.points[close_i]
                if not close_point.is_end():
                    continue
                if open_point.event is close_point.event:
                    old_event = open_point.event
                    event = ParentEvent(
                        old_event.id,
                        open_point.timestamp,
                        close_point.timestamp - open_point.timestamp,
                        old_event.data
                    )
                    events.append(Event(event, open_point.event_type))
                    break

        return events
