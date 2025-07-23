from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from freezegun import freeze_time

from ics import Calendar, Event
from ics.timezone import UTC


@pytest.fixture
def calendar() -> Calendar:
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
def __tmp6() -> Calendar:
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


def __tmp3(calendar: Calendar) -> None:
    """Test chronological iteration of a timeline."""
    assert [e.summary for e in calendar.timeline] == [
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
def __tmp4(
    calendar: Calendar, __tmp0: date | __typ0, expected_events
) -> None:
    """Test returning events on a particualr day."""
    assert [e.summary for e in calendar.timeline.on(__tmp0)] == expected_events


def test_start_after(calendar: Calendar) -> None:
    """Test chronological iteration starting at a specific time."""
    assert [e.summary for e in calendar.timeline.start_after(date(2000, 1, 1))] == [
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
def __tmp1(
    __tmp6: Calendar, __tmp5: __typ0, expected_events: list[str]
) -> None:
    """Test returning events at a specific time."""
    assert [
        e.summary for e in __tmp6.timeline.at(__tmp5)
    ] == expected_events


@freeze_time("2000-01-01 12:30:00")
def __tmp2(__tmp6: <FILL>) -> None:
    assert [e.summary for e in __tmp6.timeline.now()] == ["second"]


@freeze_time("2000-01-01 13:00:00")
def test_now_no_match(__tmp6: Calendar) -> None:
    assert [e.summary for e in __tmp6.timeline.now()] == []


@freeze_time("2000-01-01 12:30:00")
def test_today(__tmp6: Calendar) -> None:
    assert [e.summary for e in __tmp6.timeline.today()] == ["first", "second"]


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
    __tmp6: Calendar, start: __typ0, end: __typ0, expected_events: list[str]
) -> None:
    assert [
        e.summary for e in __tmp6.timeline.included(start, end)
    ] == expected_events
