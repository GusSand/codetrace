from typing import TypeAlias
__typ2 : TypeAlias = "TimedeltaLike"
__typ0 : TypeAlias = "DatetimeLike"
__typ1 : TypeAlias = "datetime"
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
def __tmp11(__tmp5: None) -> None:
    ...


@overload
def __tmp11(__tmp5) :
    ...


def __tmp11(__tmp5):
    if __tmp5 is None:
        return None
    elif isinstance(__tmp5, __typ1):
        return __tmp5
    elif isinstance(__tmp5, date):
        return __typ1.combine(__tmp5, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp5, tuple):
        return __typ1(*__tmp5)
    elif isinstance(__tmp5, dict):
        return __typ1(**__tmp5)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp5)}")


@overload
def __tmp1(__tmp5) -> None:
    ...


@overload
def __tmp1(__tmp5) :
    ...


def __tmp1(__tmp5):
    if __tmp5 is None:
        return None
    elif isinstance(__tmp5, timedelta):
        return __tmp5
    elif isinstance(__tmp5, tuple):
        return timedelta(*__tmp5)
    elif isinstance(__tmp5, dict):
        return timedelta(**__tmp5)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp5)}")


###############################################################################
# Rounding Utils


def __tmp9(td) :
    return -MAX_TIMEDELTA_NEARLY_ZERO <= td <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp2(__tmp5: __typ1) :
    ...


@overload
def __tmp2(__tmp5) :
    ...


@overload
def __tmp2(__tmp5) :
    ...


def __tmp2(__tmp5):
    if __tmp5 is None:
        return None
    if isinstance(__tmp5, date) and not isinstance(__tmp5, __typ1):
        return __tmp5
    return __typ1.combine(
        __tmp11(__tmp5).date(), MIDNIGHT, tzinfo=__tmp5.tzinfo
    )


@overload
def __tmp14(__tmp5) :
    ...


@overload
def __tmp14(__tmp5) :
    ...


@overload
def __tmp14(__tmp5) :
    ...


def __tmp14(__tmp5):
    if __tmp5 is None:
        return None
    if isinstance(__tmp5, date) and not isinstance(__tmp5, __typ1):
        return __tmp5
    floored = __tmp2(__tmp5)
    if floored != __tmp5:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def __tmp12(__tmp5: <FILL>) -> timedelta:
    return __tmp5 - (__tmp5 % TIMEDELTA_DAY)


def ceil_timedelta_to_days(__tmp5) :
    mod = __tmp5 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp5
    else:
        return __tmp5 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def limit_str_length(__tmp0):
    return str(__tmp0)  # TODO limit_str_length


def __tmp3(it, full_str):
    try:
        return next(it)
    except StopIteration as e:
        raise ValueError(
            f"value '{full_str}' may not end with an escape sequence"
        ) from e


def uid_gen() :
    uid = str(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def __tmp6(__tmp4, __tmp10, __tmp5):
    if __tmp5 is None:
        raise ValueError(f"'{__tmp10.name}' may not be None")


def validate_truthy(__tmp4, __tmp10, __tmp5):
    if not bool(__tmp5):
        raise ValueError(f"'{__tmp10.name}' must be truthy (got {__tmp5!r})")


def __tmp8(name, __tmp5, __tmp7):
    if not isinstance(__tmp5, __tmp7):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=__tmp7,
                actual=__tmp5.__class__,
                __tmp5=__tmp5,
            ),
            name,
            __tmp7,
            __tmp5,
        )


def __tmp13(__tmp4, __tmp10, __tmp5):
    __tmp4.validate(__tmp10, __tmp5)


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
