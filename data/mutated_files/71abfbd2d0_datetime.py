from typing import TypeAlias
__typ0 : TypeAlias = "Calendar"
from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from freezegun import freeze_time

from ics import Calendar, Event
from ics.timezone import UTC


@pytest.fixture
def __tmp0() :
    """Fixture calendar with all day events to use in tests."""
    cal = __typ0()
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
def __tmp8() :
    """Fixture calendar with datetime based events to use in tests."""
    cal = __typ0()
    cal.events.extend(
        [
            Event(
                "first",
                begin=datetime(2000, 1, 1, 11, 0),
                end=datetime(2000, 1, 1, 11, 30),
            ),
            Event(
                "second",
                begin=datetime(2000, 1, 1, 12, 0),
                end=datetime(2000, 1, 1, 13, 0),
            ),
            Event(
                "third",
                begin=datetime(2000, 1, 2, 12, 0),
                end=datetime(2000, 1, 2, 13, 0),
            ),
        ]
    )
    return cal


def test_iteration(__tmp0) :
    """Test chronological iteration of a timeline."""
    assert [e.summary for e in __tmp0.timeline] == [
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
        (datetime(2000, 3, 1, 6, 0), ["third"]),
    ],
)
def __tmp5(
    __tmp0, when, __tmp4
) :
    """Test returning events on a particualr day."""
    assert [e.summary for e in __tmp0.timeline.on(when)] == __tmp4


def __tmp2(__tmp0) :
    """Test chronological iteration starting at a specific time."""
    assert [e.summary for e in __tmp0.timeline.start_after(date(2000, 1, 1))] == [
        "second",
        "third",
        "fourth",
    ]


@pytest.mark.parametrize(
    "at_datetime,expected_events",
    [
        (datetime(2000, 1, 1, 11, 15), ["first"]),
        (datetime(2000, 1, 1, 11, 59), []),
        (datetime(2000, 1, 1, 12, 0), ["second"]),
        (datetime(2000, 1, 1, 12, 30), ["second"]),
        (datetime(2000, 1, 1, 12, 59), ["second"]),
        (datetime(2000, 1, 1, 13, 0), []),
    ],
)
def test_at(
    __tmp8, __tmp7, __tmp4
) :
    """Test returning events at a specific time."""
    assert [
        e.summary for e in __tmp8.timeline.at(__tmp7)
    ] == __tmp4


@freeze_time("2000-01-01 12:30:00")
def __tmp3(__tmp8) :
    assert [e.summary for e in __tmp8.timeline.now()] == ["second"]


@freeze_time("2000-01-01 13:00:00")
def __tmp1(__tmp8) :
    assert [e.summary for e in __tmp8.timeline.now()] == []


@freeze_time("2000-01-01 12:30:00")
def test_today(__tmp8) :
    assert [e.summary for e in __tmp8.timeline.today()] == ["first", "second"]


@pytest.mark.parametrize(
    "start,end,expected_events",
    [
        (
            datetime(2000, 1, 1, 10, 00),
            datetime(2000, 1, 2, 14, 00),
            ["first", "second", "third"],
        ),
        (
            datetime(2000, 1, 1, 10, 00),
            datetime(2000, 1, 1, 14, 00),
            ["first", "second"],
        ),
        (
            datetime(2000, 1, 1, 12, 00),
            datetime(2000, 1, 2, 14, 00),
            ["second", "third"],
        ),
        (datetime(2000, 1, 1, 12, 00), datetime(2000, 1, 1, 14, 00), ["second"]),
    ],
)
def __tmp6(
    __tmp8, start: <FILL>, end, __tmp4
) :
    assert [
        e.summary for e in __tmp8.timeline.included(start, end)
    ] == __tmp4
