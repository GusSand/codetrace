from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "timedelta"
__typ4 : TypeAlias = "datetime"
__typ0 : TypeAlias = "TimedeltaLike"
__typ3 : TypeAlias = "DatetimeLike"
from datetime import date, datetime, time, timedelta, timezone
from typing import overload
from uuid import uuid4

from ics.types import DatetimeLike, TimedeltaLike

datetime_tzutc = timezone.utc

MIDNIGHT = time()
TIMEDELTA_ZERO = __typ2()
TIMEDELTA_DAY = __typ2(days=1)
TIMEDELTA_SECOND = __typ2(seconds=1)
TIMEDELTA_CACHE = {0: TIMEDELTA_ZERO, "day": TIMEDELTA_DAY, "second": TIMEDELTA_SECOND}
MAX_TIMEDELTA_NEARLY_ZERO = __typ2(seconds=1) / 2


@overload
def ensure_datetime(__tmp2) :
    ...


@overload
def ensure_datetime(__tmp2) :
    ...


def ensure_datetime(__tmp2):
    if __tmp2 is None:
        return None
    elif isinstance(__tmp2, __typ4):
        return __tmp2
    elif isinstance(__tmp2, date):
        return __typ4.combine(__tmp2, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp2, tuple):
        return __typ4(*__tmp2)
    elif isinstance(__tmp2, dict):
        return __typ4(**__tmp2)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp2)}")


@overload
def ensure_timedelta(__tmp2: None) :
    ...


@overload
def ensure_timedelta(__tmp2: __typ0) -> __typ2:
    ...


def ensure_timedelta(__tmp2):
    if __tmp2 is None:
        return None
    elif isinstance(__tmp2, __typ2):
        return __tmp2
    elif isinstance(__tmp2, tuple):
        return __typ2(*__tmp2)
    elif isinstance(__tmp2, dict):
        return __typ2(**__tmp2)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp2)}")


###############################################################################
# Rounding Utils


def timedelta_nearly_zero(__tmp3) :
    return -MAX_TIMEDELTA_NEARLY_ZERO <= __tmp3 <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def floor_datetime_to_midnight(__tmp2: __typ4) :
    ...


@overload
def floor_datetime_to_midnight(__tmp2: date) -> date:
    ...


@overload
def floor_datetime_to_midnight(__tmp2) -> None:
    ...


def floor_datetime_to_midnight(__tmp2):
    if __tmp2 is None:
        return None
    if isinstance(__tmp2, date) and not isinstance(__tmp2, __typ4):
        return __tmp2
    return __typ4.combine(
        ensure_datetime(__tmp2).date(), MIDNIGHT, tzinfo=__tmp2.tzinfo
    )


@overload
def ceil_datetime_to_midnight(__tmp2: __typ4) :
    ...


@overload
def ceil_datetime_to_midnight(__tmp2) -> date:
    ...


@overload
def ceil_datetime_to_midnight(__tmp2: <FILL>) -> None:
    ...


def ceil_datetime_to_midnight(__tmp2):
    if __tmp2 is None:
        return None
    if isinstance(__tmp2, date) and not isinstance(__tmp2, __typ4):
        return __tmp2
    floored = floor_datetime_to_midnight(__tmp2)
    if floored != __tmp2:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def __tmp5(__tmp2) -> __typ2:
    return __tmp2 - (__tmp2 % TIMEDELTA_DAY)


def __tmp4(__tmp2: __typ2) :
    mod = __tmp2 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp2
    else:
        return __tmp2 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def limit_str_length(val):
    return __typ1(val)  # TODO limit_str_length


def next_after_str_escape(it, full_str):
    try:
        return next(it)
    except StopIteration as e:
        raise ValueError(
            f"value '{full_str}' may not end with an escape sequence"
        ) from e


def __tmp0() -> __typ1:
    uid = __typ1(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def validate_not_none(__tmp1, attr, __tmp2):
    if __tmp2 is None:
        raise ValueError(f"'{attr.name}' may not be None")


def validate_truthy(__tmp1, attr, __tmp2):
    if not bool(__tmp2):
        raise ValueError(f"'{attr.name}' must be truthy (got {__tmp2!r})")


def check_is_instance(name, __tmp2, clazz):
    if not isinstance(__tmp2, clazz):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=clazz,
                actual=__tmp2.__class__,
                __tmp2=__tmp2,
            ),
            name,
            clazz,
            __tmp2,
        )


def call_validate_on_inst(__tmp1, attr, __tmp2):
    __tmp1.validate(attr, __tmp2)


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
