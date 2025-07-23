from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "timedelta"
__typ0 : TypeAlias = "TimedeltaLike"
__typ5 : TypeAlias = "datetime"
__typ3 : TypeAlias = "DatetimeLike"
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
def __tmp9(__tmp4) :
    ...


@overload
def __tmp9(__tmp4) :
    ...


def __tmp9(__tmp4):
    if __tmp4 is None:
        return None
    elif isinstance(__tmp4, __typ5):
        return __tmp4
    elif isinstance(__tmp4, date):
        return __typ5.combine(__tmp4, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp4, tuple):
        return __typ5(*__tmp4)
    elif isinstance(__tmp4, dict):
        return __typ5(**__tmp4)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp4)}")


@overload
def __tmp0(__tmp4) :
    ...


@overload
def __tmp0(__tmp4) :
    ...


def __tmp0(__tmp4):
    if __tmp4 is None:
        return None
    elif isinstance(__tmp4, __typ1):
        return __tmp4
    elif isinstance(__tmp4, tuple):
        return __typ1(*__tmp4)
    elif isinstance(__tmp4, dict):
        return __typ1(**__tmp4)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp4)}")


###############################################################################
# Rounding Utils


def __tmp7(td) :
    return -MAX_TIMEDELTA_NEARLY_ZERO <= td <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def __tmp1(__tmp4) :
    ...


@overload
def __tmp1(__tmp4) :
    ...


@overload
def __tmp1(__tmp4: <FILL>) :
    ...


def __tmp1(__tmp4):
    if __tmp4 is None:
        return None
    if isinstance(__tmp4, date) and not isinstance(__tmp4, __typ5):
        return __tmp4
    return __typ5.combine(
        __tmp9(__tmp4).date(), MIDNIGHT, tzinfo=__tmp4.tzinfo
    )


@overload
def __tmp10(__tmp4) :
    ...


@overload
def __tmp10(__tmp4: date) :
    ...


@overload
def __tmp10(__tmp4) :
    ...


def __tmp10(__tmp4):
    if __tmp4 is None:
        return None
    if isinstance(__tmp4, date) and not isinstance(__tmp4, __typ5):
        return __tmp4
    floored = __tmp1(__tmp4)
    if floored != __tmp4:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def floor_timedelta_to_days(__tmp4) -> __typ1:
    return __tmp4 - (__tmp4 % TIMEDELTA_DAY)


def ceil_timedelta_to_days(__tmp4) :
    mod = __tmp4 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp4
    else:
        return __tmp4 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def limit_str_length(val):
    return __typ2(val)  # TODO limit_str_length


def __tmp2(it, full_str):
    try:
        return next(it)
    except StopIteration as e:
        raise ValueError(
            f"value '{full_str}' may not end with an escape sequence"
        ) from e


def uid_gen() :
    uid = __typ2(uuid4())
    return f"{uid}@{uid[:4]}.org"


###############################################################################


def __tmp5(__tmp3, __tmp8, __tmp4):
    if __tmp4 is None:
        raise ValueError(f"'{__tmp8.name}' may not be None")


def __tmp6(__tmp3, __tmp8, __tmp4):
    if not __typ4(__tmp4):
        raise ValueError(f"'{__tmp8.name}' must be truthy (got {__tmp4!r})")


def check_is_instance(name, __tmp4, clazz):
    if not isinstance(__tmp4, clazz):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=clazz,
                actual=__tmp4.__class__,
                __tmp4=__tmp4,
            ),
            name,
            clazz,
            __tmp4,
        )


def call_validate_on_inst(__tmp3, __tmp8, __tmp4):
    __tmp3.validate(__tmp8, __tmp4)


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
