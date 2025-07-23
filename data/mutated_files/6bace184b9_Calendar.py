from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from freezegun import freeze_time

from ics import Calendar, Event
from ics.timezone import UTC


@pytest.fixture
def __tmp1() -> Calendar:
    """Fixture calendar with all day events to use in tests."""
    cal = Calendar()
    cal.events.extend(
        [
            Event("second", date(2000, 2, 1), date(2000, 2, 2)),
            Event("fourth", date(2000, 4, 1), date(2000, 4, 2)),
            Event("third", date(2000, 3, 1), date(2000, 3, 2)),
            Event("first", date(2000, 1, 1), date(2000, 1, 2)),
        ]
    )
    for e in cal.events:
        e.make_all_day()
    return cal


@pytest.fixture
def calendar_times() :
    """Fixture calendar with datetime based events to use in tests."""
    cal = Calendar()
    cal.events.extend(
        [
            Event(
                "first",
                begin=__typ0(2000, 1, 1, 11, 0),
                end=__typ0(2000, 1, 1, 11, 30),
            ),
            Event(
                "second",
                begin=__typ0(2000, 1, 1, 12, 0),
                end=__typ0(2000, 1, 1, 13, 0),
            ),
            Event(
                "third",
                begin=__typ0(2000, 1, 2, 12, 0),
                end=__typ0(2000, 1, 2, 13, 0),
            ),
        ]
    )
    return cal


def test_iteration(__tmp1: <FILL>) -> None:
    """Test chronological iteration of a timeline."""
    assert [e.summary for e in __tmp1.timeline] == [
        "first",
        "second",
        "third",
        "fourth",
    ]


@pytest.mark.parametrize(
    "when,expected_events",
    [
        (date(2000, 1, 1), ["first"]),
        (date(2000, 2, 1), ["second"]),
        (__typ0(2000, 3, 1, 6, 0), ["third"]),
    ],
)
def test_on(
    __tmp1, when: date | __typ0, __tmp0
) :
    """Test returning events on a particualr day."""
    assert [e.summary for e in __tmp1.timeline.on(when)] == __tmp0


def test_start_after(__tmp1) :
    """Test chronological iteration starting at a specific time."""
    assert [e.summary for e in __tmp1.timeline.start_after(date(2000, 1, 1))] == [
        "second",
        "third",
        "fourth",
    ]


@pytest.mark.parametrize(
    "at_datetime,expected_events",
    [
        (__typ0(2000, 1, 1, 11, 15), ["first"]),
        (__typ0(2000, 1, 1, 11, 59), []),
        (__typ0(2000, 1, 1, 12, 0), ["second"]),
        (__typ0(2000, 1, 1, 12, 30), ["second"]),
        (__typ0(2000, 1, 1, 12, 59), ["second"]),
        (__typ0(2000, 1, 1, 13, 0), []),
    ],
)
def test_at(
    calendar_times, at_datetime: __typ0, __tmp0
) :
    """Test returning events at a specific time."""
    assert [
        e.summary for e in calendar_times.timeline.at(at_datetime)
    ] == __tmp0


@freeze_time("2000-01-01 12:30:00")
def test_now(calendar_times) -> None:
    assert [e.summary for e in calendar_times.timeline.now()] == ["second"]


@freeze_time("2000-01-01 13:00:00")
def test_now_no_match(calendar_times: Calendar) -> None:
    assert [e.summary for e in calendar_times.timeline.now()] == []


@freeze_time("2000-01-01 12:30:00")
def __tmp2(calendar_times: Calendar) -> None:
    assert [e.summary for e in calendar_times.timeline.today()] == ["first", "second"]


@pytest.mark.parametrize(
    "start,end,expected_events",
    [
        (
            __typ0(2000, 1, 1, 10, 00),
            __typ0(2000, 1, 2, 14, 00),
            ["first", "second", "third"],
        ),
        (
            __typ0(2000, 1, 1, 10, 00),
            __typ0(2000, 1, 1, 14, 00),
            ["first", "second"],
        ),
        (
            __typ0(2000, 1, 1, 12, 00),
            __typ0(2000, 1, 2, 14, 00),
            ["second", "third"],
        ),
        (__typ0(2000, 1, 1, 12, 00), __typ0(2000, 1, 1, 14, 00), ["second"]),
    ],
)
def test_included(
    calendar_times, start, end, __tmp0: list[str]
) -> None:
    assert [
        e.summary for e in calendar_times.timeline.included(start, end)
    ] == __tmp0
