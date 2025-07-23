from typing import TypeAlias
__typ0 : TypeAlias = "DatetimeLike"
__typ2 : TypeAlias = "timedelta"
__typ3 : TypeAlias = "TimedeltaLike"
__typ1 : TypeAlias = "datetime"
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
def __tmp11(__tmp9: None) -> None:
    ...


@overload
def __tmp11(__tmp9: __typ0) :
    ...


def __tmp11(__tmp9):
    if __tmp9 is None:
        return None
    elif isinstance(__tmp9, __typ1):
        return __tmp9
    elif isinstance(__tmp9, date):
        return __typ1.combine(__tmp9, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp9, tuple):
        return __typ1(*__tmp9)
    elif isinstance(__tmp9, dict):
        return __typ1(**__tmp9)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp9)}")


@overload
def __tmp3(__tmp9: <FILL>) -> None:
    ...


@overload
def __tmp3(__tmp9: __typ3) -> __typ2:
    ...


def __tmp3(__tmp9):
    if __tmp9 is None:
        return None
    elif isinstance(__tmp9, __typ2):
        return __tmp9
    elif isinstance(__tmp9, tuple):
        return __typ2(*__tmp9)
    elif isinstance(__tmp9, dict):
        return __typ2(**__tmp9)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp9)}")


###############################################################################
# Rounding Utils


def __tmp1(__tmp15: __typ2) -> bool:
    return -MAX_TIMEDELTA_NEARLY_ZERO <= __tmp15 <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp4(__tmp9) -> __typ1:
    ...


@overload
def __tmp4(__tmp9: date) -> date:
    ...


@overload
def __tmp4(__tmp9) -> None:
    ...


def __tmp4(__tmp9):
    if __tmp9 is None:
        return None
    if isinstance(__tmp9, date) and not isinstance(__tmp9, __typ1):
        return __tmp9
    return __typ1.combine(
        __tmp11(__tmp9).date(), MIDNIGHT, tzinfo=__tmp9.tzinfo
    )


@overload
def __tmp18(__tmp9: __typ1) -> __typ1:
    ...


@overload
def __tmp18(__tmp9: date) -> date:
    ...


@overload
def __tmp18(__tmp9) -> None:
    ...


def __tmp18(__tmp9):
    if __tmp9 is None:
        return None
    if isinstance(__tmp9, date) and not isinstance(__tmp9, __typ1):
        return __tmp9
    floored = __tmp4(__tmp9)
    if floored != __tmp9:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def __tmp17(__tmp9: __typ2) -> __typ2:
    return __tmp9 - (__tmp9 % TIMEDELTA_DAY)


def ceil_timedelta_to_days(__tmp9) -> __typ2:
    mod = __tmp9 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp9
    else:
        return __tmp9 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def __tmp6(__tmp13):
    return str(__tmp13)  # TODO limit_str_length


def __tmp7(__tmp14, __tmp12):
    try:
        return next(__tmp14)
    except StopIteration as e:
        raise ValueError(
            f"value '{__tmp12}' may not end with an escape sequence"
        ) from e


def uid_gen() -> str:
    uid = str(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def __tmp5(__tmp10, __tmp16, __tmp9):
    if __tmp9 is None:
        raise ValueError(f"'{__tmp16.name}' may not be None")


def __tmp0(__tmp10, __tmp16, __tmp9):
    if not bool(__tmp9):
        raise ValueError(f"'{__tmp16.name}' must be truthy (got {__tmp9!r})")


def check_is_instance(name, __tmp9, __tmp8):
    if not isinstance(__tmp9, __tmp8):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=__tmp8,
                actual=__tmp9.__class__,
                __tmp9=__tmp9,
            ),
            name,
            __tmp8,
            __tmp9,
        )


def __tmp2(__tmp10, __tmp16, __tmp9):
    __tmp10.validate(__tmp16, __tmp9)


def one(
    iterable,
    too_short="Too few items in iterable, expected one but got zero!",
    too_long="Expected exactly one item in iterable, but got {first!r}, {second!r}, and possibly more!",
):
    __tmp14 = iter(iterable)
    try:
        first = next(__tmp14)
    except StopIteration as e:
        raise ValueError(too_short.format(iter=__tmp14)) from e
    try:
        second = next(__tmp14)
    except StopIteration:
        return first
    raise ValueError(too_long.format(first=first, second=second, iter=__tmp14))
