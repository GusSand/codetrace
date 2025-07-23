from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
from datetime import date, datetime, time, timedelta, timezone
from typing import overload
from uuid import uuid4

from ics.types import DatetimeLike, TimedeltaLike

datetime_tzutc = timezone.utc

MIDNIGHT = time()
TIMEDELTA_ZERO = timedelta()
TIMEDELTA_DAY = timedelta(days=1)
TIMEDELTA_SECOND = timedelta(seconds=1)
TIMEDELTA_CACHE = {0: TIMEDELTA_ZERO, "day": TIMEDELTA_DAY, "second": TIMEDELTA_SECOND}
MAX_TIMEDELTA_NEARLY_ZERO = timedelta(seconds=1) / 2


@overload
def __tmp9(__tmp3: None) -> None:
    ...


@overload
def __tmp9(__tmp3: DatetimeLike) -> __typ0:
    ...


def __tmp9(__tmp3):
    if __tmp3 is None:
        return None
    elif isinstance(__tmp3, __typ0):
        return __tmp3
    elif isinstance(__tmp3, date):
        return __typ0.combine(__tmp3, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp3, tuple):
        return __typ0(*__tmp3)
    elif isinstance(__tmp3, dict):
        return __typ0(**__tmp3)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp3)}")


@overload
def __tmp0(__tmp3: None) -> None:
    ...


@overload
def __tmp0(__tmp3: TimedeltaLike) :
    ...


def __tmp0(__tmp3):
    if __tmp3 is None:
        return None
    elif isinstance(__tmp3, timedelta):
        return __tmp3
    elif isinstance(__tmp3, tuple):
        return timedelta(*__tmp3)
    elif isinstance(__tmp3, dict):
        return timedelta(**__tmp3)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp3)}")


###############################################################################
# Rounding Utils


def __tmp6(__tmp4) -> bool:
    return -MAX_TIMEDELTA_NEARLY_ZERO <= __tmp4 <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp1(__tmp3: __typ0) -> __typ0:
    ...


@overload
def __tmp1(__tmp3: date) -> date:
    ...


@overload
def __tmp1(__tmp3: None) -> None:
    ...


def __tmp1(__tmp3):
    if __tmp3 is None:
        return None
    if isinstance(__tmp3, date) and not isinstance(__tmp3, __typ0):
        return __tmp3
    return __typ0.combine(
        __tmp9(__tmp3).date(), MIDNIGHT, tzinfo=__tmp3.tzinfo
    )


@overload
def __tmp10(__tmp3: __typ0) -> __typ0:
    ...


@overload
def __tmp10(__tmp3: date) -> date:
    ...


@overload
def __tmp10(__tmp3: None) -> None:
    ...


def __tmp10(__tmp3):
    if __tmp3 is None:
        return None
    if isinstance(__tmp3, date) and not isinstance(__tmp3, __typ0):
        return __tmp3
    floored = __tmp1(__tmp3)
    if floored != __tmp3:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def floor_timedelta_to_days(__tmp3: timedelta) -> timedelta:
    return __tmp3 - (__tmp3 % TIMEDELTA_DAY)


def __tmp8(__tmp3: <FILL>) -> timedelta:
    mod = __tmp3 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp3
    else:
        return __tmp3 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def limit_str_length(val):
    return str(val)  # TODO limit_str_length


def next_after_str_escape(it, __tmp11):
    try:
        return next(it)
    except StopIteration as e:
        raise ValueError(
            f"value '{__tmp11}' may not end with an escape sequence"
        ) from e


def uid_gen() -> str:
    uid = str(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def validate_not_none(__tmp2, __tmp7, __tmp3):
    if __tmp3 is None:
        raise ValueError(f"'{__tmp7.name}' may not be None")


def validate_truthy(__tmp2, __tmp7, __tmp3):
    if not bool(__tmp3):
        raise ValueError(f"'{__tmp7.name}' must be truthy (got {__tmp3!r})")


def check_is_instance(name, __tmp3, clazz):
    if not isinstance(__tmp3, clazz):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=clazz,
                actual=__tmp3.__class__,
                __tmp3=__tmp3,
            ),
            name,
            clazz,
            __tmp3,
        )


def __tmp5(__tmp2, __tmp7, __tmp3):
    __tmp2.validate(__tmp7, __tmp3)


def one(
    iterable,
    too_short="Too few items in iterable, expected one but got zero!",
    too_long="Expected exactly one item in iterable, but got {first!r}, {second!r}, and possibly more!",
):
    it = iter(iterable)
    try:
        first = next(it)
    except StopIteration as e:
        raise ValueError(too_short.format(iter=it)) from e
    try:
        second = next(it)
    except StopIteration:
        return first
    raise ValueError(too_long.format(first=first, second=second, iter=it))
