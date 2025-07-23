from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "timedelta"
__typ0 : TypeAlias = "TimedeltaLike"
__typ5 : TypeAlias = "datetime"
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
def ensure_datetime(__tmp3: None) -> None:
    ...


@overload
def ensure_datetime(__tmp3: __typ3) :
    ...


def ensure_datetime(__tmp3):
    if __tmp3 is None:
        return None
    elif isinstance(__tmp3, __typ5):
        return __tmp3
    elif isinstance(__tmp3, date):
        return __typ5.combine(__tmp3, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp3, tuple):
        return __typ5(*__tmp3)
    elif isinstance(__tmp3, dict):
        return __typ5(**__tmp3)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp3)}")


@overload
def __tmp0(__tmp3: None) -> None:
    ...


@overload
def __tmp0(__tmp3: __typ0) -> __typ2:
    ...


def __tmp0(__tmp3):
    if __tmp3 is None:
        return None
    elif isinstance(__tmp3, __typ2):
        return __tmp3
    elif isinstance(__tmp3, tuple):
        return __typ2(*__tmp3)
    elif isinstance(__tmp3, dict):
        return __typ2(**__tmp3)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp3)}")


###############################################################################
# Rounding Utils


def timedelta_nearly_zero(td: __typ2) -> __typ4:
    return -MAX_TIMEDELTA_NEARLY_ZERO <= td <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp1(__tmp3: __typ5) -> __typ5:
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
    if isinstance(__tmp3, date) and not isinstance(__tmp3, __typ5):
        return __tmp3
    return __typ5.combine(
        ensure_datetime(__tmp3).date(), MIDNIGHT, tzinfo=__tmp3.tzinfo
    )


@overload
def ceil_datetime_to_midnight(__tmp3: __typ5) -> __typ5:
    ...


@overload
def ceil_datetime_to_midnight(__tmp3: <FILL>) -> date:
    ...


@overload
def ceil_datetime_to_midnight(__tmp3: None) -> None:
    ...


def ceil_datetime_to_midnight(__tmp3):
    if __tmp3 is None:
        return None
    if isinstance(__tmp3, date) and not isinstance(__tmp3, __typ5):
        return __tmp3
    floored = __tmp1(__tmp3)
    if floored != __tmp3:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def floor_timedelta_to_days(__tmp3: __typ2) -> __typ2:
    return __tmp3 - (__tmp3 % TIMEDELTA_DAY)


def ceil_timedelta_to_days(__tmp3) -> __typ2:
    mod = __tmp3 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp3
    else:
        return __tmp3 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def __tmp5(val):
    return __typ1(val)  # TODO limit_str_length


def next_after_str_escape(it, full_str):
    try:
        return next(it)
    except StopIteration as e:
        raise ValueError(
            f"value '{full_str}' may not end with an escape sequence"
        ) from e


def uid_gen() -> __typ1:
    uid = __typ1(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def validate_not_none(__tmp2, __tmp4, __tmp3):
    if __tmp3 is None:
        raise ValueError(f"'{__tmp4.name}' may not be None")


def validate_truthy(__tmp2, __tmp4, __tmp3):
    if not __typ4(__tmp3):
        raise ValueError(f"'{__tmp4.name}' must be truthy (got {__tmp3!r})")


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


def __tmp6(__tmp2, __tmp4, __tmp3):
    __tmp2.validate(__tmp4, __tmp3)


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
