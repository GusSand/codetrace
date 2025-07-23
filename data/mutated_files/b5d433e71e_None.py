from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "timedelta"
from datetime import date, datetime, time, timedelta, timezone
from typing import overload
from uuid import uuid4

from ics.types import DatetimeLike, TimedeltaLike

datetime_tzutc = timezone.utc

MIDNIGHT = time()
TIMEDELTA_ZERO = __typ1()
TIMEDELTA_DAY = __typ1(days=1)
TIMEDELTA_SECOND = __typ1(seconds=1)
TIMEDELTA_CACHE = {0: TIMEDELTA_ZERO, "day": TIMEDELTA_DAY, "second": TIMEDELTA_SECOND}
MAX_TIMEDELTA_NEARLY_ZERO = __typ1(seconds=1) / 2


@overload
def __tmp8(__tmp5: <FILL>) :
    ...


@overload
def __tmp8(__tmp5) :
    ...


def __tmp8(__tmp5):
    if __tmp5 is None:
        return None
    elif isinstance(__tmp5, __typ0):
        return __tmp5
    elif isinstance(__tmp5, date):
        return __typ0.combine(__tmp5, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp5, tuple):
        return __typ0(*__tmp5)
    elif isinstance(__tmp5, dict):
        return __typ0(**__tmp5)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp5)}")


@overload
def __tmp1(__tmp5) :
    ...


@overload
def __tmp1(__tmp5) :
    ...


def __tmp1(__tmp5):
    if __tmp5 is None:
        return None
    elif isinstance(__tmp5, __typ1):
        return __tmp5
    elif isinstance(__tmp5, tuple):
        return __typ1(*__tmp5)
    elif isinstance(__tmp5, dict):
        return __typ1(**__tmp5)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp5)}")


###############################################################################
# Rounding Utils


def timedelta_nearly_zero(td) :
    return -MAX_TIMEDELTA_NEARLY_ZERO <= td <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp2(__tmp5) :
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
    if isinstance(__tmp5, date) and not isinstance(__tmp5, __typ0):
        return __tmp5
    return __typ0.combine(
        __tmp8(__tmp5).date(), MIDNIGHT, tzinfo=__tmp5.tzinfo
    )


@overload
def __tmp11(__tmp5) :
    ...


@overload
def __tmp11(__tmp5) :
    ...


@overload
def __tmp11(__tmp5) :
    ...


def __tmp11(__tmp5):
    if __tmp5 is None:
        return None
    if isinstance(__tmp5, date) and not isinstance(__tmp5, __typ0):
        return __tmp5
    floored = __tmp2(__tmp5)
    if floored != __tmp5:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def floor_timedelta_to_days(__tmp5) :
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


def next_after_str_escape(it, __tmp10):
    try:
        return next(it)
    except StopIteration as e:
        raise ValueError(
            f"value '{__tmp10}' may not end with an escape sequence"
        ) from e


def __tmp3() :
    uid = str(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def validate_not_none(__tmp6, attr, __tmp5):
    if __tmp5 is None:
        raise ValueError(f"'{attr.name}' may not be None")


def __tmp7(__tmp6, attr, __tmp5):
    if not __typ2(__tmp5):
        raise ValueError(f"'{attr.name}' must be truthy (got {__tmp5!r})")


def check_is_instance(name, __tmp5, __tmp4):
    if not isinstance(__tmp5, __tmp4):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=__tmp4,
                actual=__tmp5.__class__,
                __tmp5=__tmp5,
            ),
            name,
            __tmp4,
            __tmp5,
        )


def __tmp9(__tmp6, attr, __tmp5):
    __tmp6.validate(attr, __tmp5)


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
