from typing import TypeAlias
__typ2 : TypeAlias = "int"
__typ5 : TypeAlias = "Any"
import warnings
from datetime import date, datetime, timedelta
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterator,
    List,
    MutableMapping,
    NewType,
    Optional,
    Tuple,
    Union,
    cast,
    overload,
)
from urllib.parse import ParseResult

import attr

if TYPE_CHECKING:
    # noinspection PyUnresolvedReferences
    # noinspection PyUnresolvedReferences
    from ics.contentline import Container, ContentLine
    from ics.event import CalendarEntryAttrs, Event

    # noinspection PyUnresolvedReferences
    from ics.timespan import Timespan

    # noinspection PyUnresolvedReferences
    from ics.todo import Todo

__all__ = [
    "ContainerItem",
    "ContainerList",
    "URL",
    "DatetimeLike",
    "OptionalDatetimeLike",
    "TimedeltaLike",
    "OptionalTimedeltaLike",
    "TimespanOrBegin",
    "EventOrTimespan",
    "EventOrTimespanOrInstant",
    "TodoOrTimespan",
    "TodoOrTimespanOrInstant",
    "CalendarEntryOrTimespan",
    "CalendarEntryOrTimespanOrInstant",
    "get_timespan_if_calendar_entry",
    "RuntimeAttrValidation",
    "EmptyDict",
    "ExtraParams",
    "EmptyParams",
    "ContextDict",
    "EmptyContext",
    "copy_extra_params",
]

ContainerItem = Union["ContentLine", "Container"]
ContainerList = List[ContainerItem]
URL = ParseResult


class UTCOffsetMeta(type):
    def __instancecheck__(__tmp4, __tmp3):
        return isinstance(__tmp3, timedelta)


class UTCOffset(timedelta, metaclass=UTCOffsetMeta):
    pass


DatetimeLike = Union[Tuple, Dict, datetime, date]
OptionalDatetimeLike = Union[Tuple, Dict, datetime, date, None]
TimedeltaLike = Union[Tuple, Dict, timedelta]
OptionalTimedeltaLike = Union[Tuple, Dict, timedelta, None]

TimespanOrBegin = Union[datetime, date, "Timespan"]
EventOrTimespan = Union["Event", "Timespan"]
EventOrTimespanOrInstant = Union["Event", "Timespan", datetime]
TodoOrTimespan = Union["Todo", "Timespan"]
TodoOrTimespanOrInstant = Union["Todo", "Timespan", datetime]
__typ1 = Union["CalendarEntryAttrs", "Timespan"]
CalendarEntryOrTimespanOrInstant = Union["CalendarEntryAttrs", "Timespan", datetime]


@overload
def get_timespan_if_calendar_entry(__tmp2) :
    ...


@overload
def get_timespan_if_calendar_entry(__tmp2: <FILL>) :
    ...


@overload
def get_timespan_if_calendar_entry(__tmp2) :
    ...


def get_timespan_if_calendar_entry(__tmp2):
    from ics.event import (  # noqa: F811 # pyflakes considers this a redef of the unused if TYPE_CHECKING import above
        CalendarEntryAttrs,
    )

    if isinstance(__tmp2, CalendarEntryAttrs):
        return __tmp2.timespan
    else:
        return __tmp2


@attr.s
class __typ4:
    """
    Mixin that automatically calls the converters and validators of `attr` attributes.
    The library itself only calls these in the generated `__init__` method, with
    this mixin they are also called when later (re-)assigning an attribute, which
    is handled by `__setattr__`. This makes setting attributes as versatile as specifying
    them as init parameters and also ensures that the guarantees of validators are
    preserved even after creation of the object, at a small runtime cost.
    """

    def __attrs_post_init__(__tmp1):
        object.__setattr__(__tmp1, "__post_init__", True)

    def __setattr__(__tmp1, key, __tmp2):
        if getattr(__tmp1, "__post_init__", None):
            __tmp4 = __tmp1.__class__  # type: Any
            if not getattr(__tmp4, "__attr_fields__", None):
                __tmp4.__attr_fields__ = attr.fields_dict(__tmp4)
            try:
                field = __tmp4.__attr_fields__[key]
            except KeyError:
                pass
            else:  # when no KeyError was thrown
                if field.converter is not None:
                    __tmp2 = field.converter(__tmp2)
                if field.validator is not None:
                    field.validator(__tmp1, field, __tmp2)
        super().__setattr__(key, __tmp2)


class __typ3(MutableMapping[__typ5, None]):
    """An empty, immutable dict that returns `None` for any key. Useful as default value for function arguments."""

    def __tmp0(__tmp1, k) :
        return None

    def __setitem__(__tmp1, k, v) :
        warnings.warn(f"{__tmp1.__class__.__name__}[{k!r}] = {v} ignored")
        return

    def __delitem__(__tmp1, v) :
        warnings.warn(f"del {__tmp1.__class__.__name__}[{v!r}] ignored")
        return

    def __len__(__tmp1) :
        return 0

    def __tmp5(__tmp1) :
        return iter([])


EmptyDict = __typ3()
__typ0 = NewType("ExtraParams", Dict[str, List[str]])
EmptyParams = cast("ExtraParams", EmptyDict)
ContextDict = NewType("ContextDict", Dict[__typ5, __typ5])  # defaultdict(lambda: None)
EmptyContext = cast("ContextDict", EmptyDict)


def copy_extra_params(old) :
    new: __typ0 = __typ0(dict())
    if not old:
        return new
    for key, __tmp2 in old.items():
        if isinstance(__tmp2, str):
            new[key] = __tmp2
        elif isinstance(__tmp2, list):
            new[key] = list(__tmp2)
        else:
            raise ValueError(
                "can't convert extra param {} with value of type {}: {}".format(
                    key, type(__tmp2), __tmp2
                )
            )
    return new
