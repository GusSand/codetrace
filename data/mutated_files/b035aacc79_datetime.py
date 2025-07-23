from typing import TypeAlias
__typ1 : TypeAlias = "TimedeltaLike"
__typ0 : TypeAlias = "timedelta"
from datetime import date, datetime, time, timedelta, timezone
from typing import overload
from uuid import uuid4

from ics.types import DatetimeLike, TimedeltaLike

datetime_tzutc = timezone.utc

MIDNIGHT = time()
TIMEDELTA_ZERO = __typ0()
TIMEDELTA_DAY = __typ0(days=1)
TIMEDELTA_SECOND = __typ0(seconds=1)
TIMEDELTA_CACHE = {0: TIMEDELTA_ZERO, "day": TIMEDELTA_DAY, "second": TIMEDELTA_SECOND}
MAX_TIMEDELTA_NEARLY_ZERO = __typ0(seconds=1) / 2


@overload
def __tmp13(__tmp11) -> None:
    ...


@overload
def __tmp13(__tmp11: DatetimeLike) -> datetime:
    ...


def __tmp13(__tmp11):
    if __tmp11 is None:
        return None
    elif isinstance(__tmp11, datetime):
        return __tmp11
    elif isinstance(__tmp11, date):
        return datetime.combine(__tmp11, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp11, tuple):
        return datetime(*__tmp11)
    elif isinstance(__tmp11, dict):
        return datetime(**__tmp11)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp11)}")


@overload
def __tmp2(__tmp11: None) :
    ...


@overload
def __tmp2(__tmp11: __typ1) -> __typ0:
    ...


def __tmp2(__tmp11):
    if __tmp11 is None:
        return None
    elif isinstance(__tmp11, __typ0):
        return __tmp11
    elif isinstance(__tmp11, tuple):
        return __typ0(*__tmp11)
    elif isinstance(__tmp11, dict):
        return __typ0(**__tmp11)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp11)}")


###############################################################################
# Rounding Utils


def timedelta_nearly_zero(__tmp17) -> bool:
    return -MAX_TIMEDELTA_NEARLY_ZERO <= __tmp17 <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp3(__tmp11: <FILL>) -> datetime:
    ...


@overload
def __tmp3(__tmp11: date) :
    ...


@overload
def __tmp3(__tmp11) -> None:
    ...


def __tmp3(__tmp11):
    if __tmp11 is None:
        return None
    if isinstance(__tmp11, date) and not isinstance(__tmp11, datetime):
        return __tmp11
    return datetime.combine(
        __tmp13(__tmp11).date(), MIDNIGHT, tzinfo=__tmp11.tzinfo
    )


@overload
def __tmp19(__tmp11: datetime) :
    ...


@overload
def __tmp19(__tmp11: date) :
    ...


@overload
def __tmp19(__tmp11) :
    ...


def __tmp19(__tmp11):
    if __tmp11 is None:
        return None
    if isinstance(__tmp11, date) and not isinstance(__tmp11, datetime):
        return __tmp11
    floored = __tmp3(__tmp11)
    if floored != __tmp11:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def floor_timedelta_to_days(__tmp11) :
    return __tmp11 - (__tmp11 % TIMEDELTA_DAY)


def __tmp12(__tmp11) :
    mod = __tmp11 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp11
    else:
        return __tmp11 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def __tmp7(__tmp15):
    return str(__tmp15)  # TODO limit_str_length


def __tmp9(__tmp16, __tmp14):
    try:
        return next(__tmp16)
    except StopIteration as e:
        raise ValueError(
            f"value '{__tmp14}' may not end with an escape sequence"
        ) from e


def __tmp4() :
    uid = str(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def __tmp5(__tmp10, __tmp18, __tmp11):
    if __tmp11 is None:
        raise ValueError(f"'{__tmp18.name}' may not be None")


def __tmp0(__tmp10, __tmp18, __tmp11):
    if not bool(__tmp11):
        raise ValueError(f"'{__tmp18.name}' must be truthy (got {__tmp11!r})")


def __tmp6(name, __tmp11, clazz):
    if not isinstance(__tmp11, clazz):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=clazz,
                actual=__tmp11.__class__,
                __tmp11=__tmp11,
            ),
            name,
            clazz,
            __tmp11,
        )


def __tmp1(__tmp10, __tmp18, __tmp11):
    __tmp10.validate(__tmp18, __tmp11)


def one(
    __tmp8,
    too_short="Too few items in iterable, expected one but got zero!",
    too_long="Expected exactly one item in iterable, but got {first!r}, {second!r}, and possibly more!",
):
    __tmp16 = iter(__tmp8)
    try:
        first = next(__tmp16)
    except StopIteration as e:
        raise ValueError(too_short.format(iter=__tmp16)) from e
    try:
        second = next(__tmp16)
    except StopIteration:
        return first
    raise ValueError(too_long.format(first=first, second=second, iter=__tmp16))
