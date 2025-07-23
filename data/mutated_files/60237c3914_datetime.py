from typing import TypeAlias
__typ0 : TypeAlias = "DatetimeLike"
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
def ensure_datetime(__tmp0: None) :
    ...


@overload
def ensure_datetime(__tmp0: __typ0) -> datetime:
    ...


def ensure_datetime(__tmp0):
    if __tmp0 is None:
        return None
    elif isinstance(__tmp0, datetime):
        return __tmp0
    elif isinstance(__tmp0, date):
        return datetime.combine(__tmp0, MIDNIGHT, tzinfo=None)
    elif isinstance(__tmp0, tuple):
        return datetime(*__tmp0)
    elif isinstance(__tmp0, dict):
        return datetime(**__tmp0)
    else:
        raise ValueError(f"can't construct datetime from {repr(__tmp0)}")


@overload
def ensure_timedelta(__tmp0: None) :
    ...


@overload
def ensure_timedelta(__tmp0) :
    ...


def ensure_timedelta(__tmp0):
    if __tmp0 is None:
        return None
    elif isinstance(__tmp0, __typ1):
        return __tmp0
    elif isinstance(__tmp0, tuple):
        return __typ1(*__tmp0)
    elif isinstance(__tmp0, dict):
        return __typ1(**__tmp0)
    else:
        raise ValueError(f"can't construct timedelta from {repr(__tmp0)}")


###############################################################################
# Rounding Utils


def timedelta_nearly_zero(td: __typ1) -> bool:
    return -MAX_TIMEDELTA_NEARLY_ZERO <= td <= MAX_TIMEDELTA_NEARLY_ZERO


@overload
def floor_datetime_to_midnight(__tmp0) :
    ...


@overload
def floor_datetime_to_midnight(__tmp0: date) :
    ...


@overload
def floor_datetime_to_midnight(__tmp0: None) -> None:
    ...


def floor_datetime_to_midnight(__tmp0):
    if __tmp0 is None:
        return None
    if isinstance(__tmp0, date) and not isinstance(__tmp0, datetime):
        return __tmp0
    return datetime.combine(
        ensure_datetime(__tmp0).date(), MIDNIGHT, tzinfo=__tmp0.tzinfo
    )


@overload
def ceil_datetime_to_midnight(__tmp0: <FILL>) :
    ...


@overload
def ceil_datetime_to_midnight(__tmp0) :
    ...


@overload
def ceil_datetime_to_midnight(__tmp0) :
    ...


def ceil_datetime_to_midnight(__tmp0):
    if __tmp0 is None:
        return None
    if isinstance(__tmp0, date) and not isinstance(__tmp0, datetime):
        return __tmp0
    floored = floor_datetime_to_midnight(__tmp0)
    if floored != __tmp0:
        return floored + TIMEDELTA_DAY
    else:
        return floored


def floor_timedelta_to_days(__tmp0) -> __typ1:
    return __tmp0 - (__tmp0 % TIMEDELTA_DAY)


def ceil_timedelta_to_days(__tmp0) :
    mod = __tmp0 % TIMEDELTA_DAY
    if mod == TIMEDELTA_ZERO:
        return __tmp0
    else:
        return __tmp0 + TIMEDELTA_DAY - mod


###############################################################################
# String Utils


def limit_str_length(val):
    return str(val)  # TODO limit_str_length


def next_after_str_escape(it, full_str):
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


def validate_not_none(inst, attr, __tmp0):
    if __tmp0 is None:
        raise ValueError(f"'{attr.name}' may not be None")


def validate_truthy(inst, attr, __tmp0):
    if not bool(__tmp0):
        raise ValueError(f"'{attr.name}' must be truthy (got {__tmp0!r})")


def check_is_instance(name, __tmp0, clazz):
    if not isinstance(__tmp0, clazz):
        raise TypeError(
            "'{name}' must be {type!r} (got {value!r} that is a "
            "{actual!r}).".format(
                name=name,
                type=clazz,
                actual=__tmp0.__class__,
                __tmp0=__tmp0,
            ),
            name,
            clazz,
            __tmp0,
        )


def call_validate_on_inst(inst, attr, __tmp0):
    inst.validate(attr, __tmp0)


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
