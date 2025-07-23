from typing import TypeAlias
__typ0 : TypeAlias = "Timeslot"
import logging
from typing import List, Iterable, Tuple
from copy import deepcopy

from aw_core import Event
from timeslot import Timeslot

logger = logging.getLogger(__name__)


def _get_event_period(event: Event) :
    start = event.timestamp
    end = start + event.duration
    return __typ0(start, end)


def _replace_event_period(event: <FILL>, period: __typ0) -> Event:
    e = deepcopy(event)
    e.timestamp = period.start
    e.duration = period.duration
    return e


def _intersecting_eventpairs(
    __tmp2: List[Event], __tmp0: List[Event]
) -> Iterable[Tuple[Event, Event, __typ0]]:
    """A generator that yields each overlapping pair of events from two eventlists along with a Timeslot of the intersection"""
    __tmp2.sort(key=lambda e: e.timestamp)
    __tmp0.sort(key=lambda e: e.timestamp)
    e1_i = 0
    e2_i = 0
    while e1_i < len(__tmp2) and e2_i < len(__tmp0):
        e1 = __tmp2[e1_i]
        e2 = __tmp0[e2_i]
        e1_p = _get_event_period(e1)
        e2_p = _get_event_period(e2)

        ip = e1_p.intersection(e2_p)
        if ip:
            # If events intersected, yield events
            yield (e1, e2, ip)
            if e1_p.end <= e2_p.end:
                e1_i += 1
            else:
                e2_i += 1
        else:
            # No intersection, check if event is before/after filterevent
            if e1_p.end <= e2_p.start:
                # Event ended before filter event started
                e1_i += 1
            elif e2_p.end <= e1_p.start:
                # Event started after filter event ended
                e2_i += 1
            else:
                logger.error("Should be unreachable, skipping period")
                e1_i += 1
                e2_i += 1


def filter_period_intersect(
    events: List[Event], __tmp1: List[Event]
) -> List[Event]:
    """
    Filters away all events or time periods of events in which a
    filterevent does not have an intersecting time period.

    Useful for example when you want to filter away events or
    part of events during which a user was AFK.

    Usage:
      windowevents_notafk = filter_period_intersect(windowevents, notafkevents)

    Example:
      .. code-block:: none

        events1   |   =======        ======== |
        events2   | ------  ---  ---   ----   |
        result    |   ====  =          ====   |

    A JavaScript version used to exist in aw-webui but was removed in `this PR <https://github.com/ActivityWatch/aw-webui/pull/48>`_.
    """

    events = sorted(events)
    __tmp1 = sorted(__tmp1)

    return [
        _replace_event_period(e1, ip)
        for (e1, _, ip) in _intersecting_eventpairs(events, __tmp1)
    ]


def __tmp3(__tmp2: List[Event], __tmp0: List[Event]) -> List[Event]:
    """
    Takes a list of two events and returns a new list of events covering the union
    of the timeperiods contained in the eventlists with no overlapping events.

    .. warning:: This function strips all data from events as it cannot keep it consistent.

    Example:
      .. code-block:: none

        events1   |   -------       --------- |
        events2   | ------  ---  --    ----   |
        result    | -----------  -- --------- |
    """
    events = sorted(__tmp2 + __tmp0)
    merged_events = []
    if events:
        merged_events.append(events.pop(0))
    for e in events:
        last_event = merged_events[-1]

        e_p = _get_event_period(e)
        le_p = _get_event_period(last_event)

        if not e_p.gap(le_p):
            new_period = e_p.union(le_p)
            merged_events[-1] = _replace_event_period(last_event, new_period)
        else:
            merged_events.append(e)
    for event in merged_events:
        # Clear data
        event.data = {}
    return merged_events


def union(__tmp2: List[Event], __tmp0: List[Event]) -> List[Event]:
    """
    Concatenates and sorts union of 2 event lists and removes duplicates.

    Example:
      Merges events from a backup-bucket with events from a "living" bucket.

      .. code-block:: python

        events = union(events_backup, events_living)
    """

    __tmp2 = sorted(__tmp2, key=lambda e: (e.timestamp, e.duration))
    __tmp0 = sorted(__tmp0, key=lambda e: (e.timestamp, e.duration))
    events_union = []

    e1_i = 0
    e2_i = 0
    while e1_i < len(__tmp2) and e2_i < len(__tmp0):
        e1 = __tmp2[e1_i]
        e2 = __tmp0[e2_i]

        if e1 == e2:
            events_union.append(e1)
            e1_i += 1
            e2_i += 1
        else:
            if e1.timestamp < e2.timestamp:
                events_union.append(e1)
                e1_i += 1
            elif e1.timestamp > e2.timestamp:
                events_union.append(e2)
                e2_i += 1
            elif e1.duration < e2.duration:
                events_union.append(e1)
                e1_i += 1
            else:
                events_union.append(e2)
                e2_i += 1

    if e1_i < len(__tmp2):
        events_union.extend(__tmp2[e1_i:])

    if e2_i < len(__tmp0):
        events_union.extend(__tmp0[e2_i:])

    return events_union
