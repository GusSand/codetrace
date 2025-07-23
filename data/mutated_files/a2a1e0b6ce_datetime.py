from typing import TypeAlias
__typ0 : TypeAlias = "timedelta"
from datetime import date, datetime, timedelta

import pytest

from ics import Calendar, Event, Timezone, Todo
from ics.event import deterministic_event_data
from ics.timezone import UTC

SUMMARY = "test summary"


@deterministic_event_data()
@pytest.mark.parametrize(
    "begin,end,duration",
    [
        (
            datetime.fromisoformat("2022-09-16 12:00"),
            datetime.fromisoformat("2022-09-16 12:30"),
            __typ0(minutes=30),
        ),
        (
            date.fromisoformat("2022-09-16"),
            date.fromisoformat("2022-09-17"),
            __typ0(hours=24),
        ),
        (
            datetime.fromisoformat("2022-09-16 06:00"),
            datetime.fromisoformat("2022-09-17 08:30"),
            __typ0(days=1, hours=2, minutes=30),
        ),
    ],
)
def __tmp5(__tmp0: datetime, end: <FILL>, duration) -> None:
    event = Event(SUMMARY, __tmp0, end)
    assert event.duration == duration


@deterministic_event_data()
def __tmp3() -> None:
    event1 = Event(SUMMARY, date(2022, 9, 6), date(2022, 9, 7))
    __tmp4 = Event(SUMMARY, date(2022, 9, 8), date(2022, 9, 10))
    assert event1 < __tmp4
    assert event1 <= __tmp4
    assert __tmp4 >= event1
    assert __tmp4 > event1


@deterministic_event_data()
def __tmp2() -> None:
    event1 = Event(SUMMARY, date(2022, 9, 6), date(2022, 9, 10))
    __tmp4 = Event(SUMMARY, date(2022, 9, 7), date(2022, 9, 8))
    event3 = Event(SUMMARY, date(2022, 9, 9), date(2022, 9, 11))

    assert not event1.starts_within(__tmp4)
    assert not event1.starts_within(event3)
    assert __tmp4.starts_within(event1)
    assert not __tmp4.starts_within(event3)
    assert event3.starts_within(event1)
    assert not event3.starts_within(__tmp4)

    assert not event1.ends_within(__tmp4)
    assert event1.ends_within(event3)
    assert __tmp4.ends_within(event1)
    assert not __tmp4.ends_within(event3)
    assert not event3.ends_within(event1)
    assert not event3.ends_within(__tmp4)
    assert __tmp4 > event1

    assert event1.includes(__tmp4)
    assert not event1.includes(event3)
    assert not __tmp4.includes(event1)
    assert not __tmp4.includes(event3)
    assert not event3.includes(event1)
    assert not event3.includes(__tmp4)

    assert not event1.is_included_in(__tmp4)
    assert not event1.is_included_in(event3)
    assert __tmp4.is_included_in(event1)
    assert not __tmp4.is_included_in(event3)
    assert not event3.is_included_in(event1)
    assert not event3.is_included_in(__tmp4)


@deterministic_event_data()
@pytest.mark.parametrize(
    "event1,event2,expect_intersects",
    [
        (
            Event(
                SUMMARY,
                date(2022, 9, 16),
                date(2022, 9, 17),
            ),
            Event(
                SUMMARY,
                date(2022, 9, 18),
                date(2022, 9, 19),
            ),
            False,
        ),
        (
            Event(
                SUMMARY,
                date(2022, 9, 16),
                date(2022, 9, 19),
            ),
            Event(
                SUMMARY,
                date(2022, 9, 17),
                date(2022, 9, 18),
            ),
            True,
        ),
        (
            Event(
                SUMMARY,
                date(2022, 9, 16),
                date(2022, 9, 18),
            ),
            Event(
                SUMMARY,
                date(2022, 9, 17),
                date(2022, 9, 19),
            ),
            True,
        ),
    ],
)
def test_intersects(event1: Event, __tmp4, __tmp1) :
    assert __tmp4.intersects(event1) == __tmp1
