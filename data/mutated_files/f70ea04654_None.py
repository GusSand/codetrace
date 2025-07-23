from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
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
    def __instancecheck__(__tmp6, __tmp4):
        return isinstance(__tmp4, timedelta)


class UTCOffset(timedelta, metaclass=UTCOffsetMeta):
    pass


DatetimeLike = Union[Tuple, Dict, __typ0, date]
OptionalDatetimeLike = Union[Tuple, Dict, __typ0, date, None]
TimedeltaLike = Union[Tuple, Dict, timedelta]
OptionalTimedeltaLike = Union[Tuple, Dict, timedelta, None]

TimespanOrBegin = Union[__typ0, date, "Timespan"]
EventOrTimespan = Union["Event", "Timespan"]
EventOrTimespanOrInstant = Union["Event", "Timespan", __typ0]
TodoOrTimespan = Union["Todo", "Timespan"]
TodoOrTimespanOrInstant = Union["Todo", "Timespan", __typ0]
CalendarEntryOrTimespan = Union["CalendarEntryAttrs", "Timespan"]
CalendarEntryOrTimespanOrInstant = Union["CalendarEntryAttrs", "Timespan", __typ0]


@overload
def __tmp7(__tmp3) -> "Timespan":
    ...


@overload
def __tmp7(__tmp3) :
    ...


@overload
def __tmp7(__tmp3: <FILL>) -> None:
    ...


def __tmp7(__tmp3):
    from ics.event import (  # noqa: F811 # pyflakes considers this a redef of the unused if TYPE_CHECKING import above
        CalendarEntryAttrs,
    )

    if isinstance(__tmp3, CalendarEntryAttrs):
        return __tmp3.timespan
    else:
        return __tmp3


@attr.s
class RuntimeAttrValidation:
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

    def __setattr__(__tmp1, key, __tmp3):
        if getattr(__tmp1, "__post_init__", None):
            __tmp6 = __tmp1.__class__  # type: Any
            if not getattr(__tmp6, "__attr_fields__", None):
                __tmp6.__attr_fields__ = attr.fields_dict(__tmp6)
            try:
                field = __tmp6.__attr_fields__[key]
            except KeyError:
                pass
            else:  # when no KeyError was thrown
                if field.converter is not None:
                    __tmp3 = field.converter(__tmp3)
                if field.validator is not None:
                    field.validator(__tmp1, field, __tmp3)
        super().__setattr__(key, __tmp3)


class EmptyDictType(MutableMapping[Any, None]):
    """An empty, immutable dict that returns `None` for any key. Useful as default value for function arguments."""

    def __tmp0(__tmp1, k: Any) :
        return None

    def __tmp2(__tmp1, k: Any, v) :
        warnings.warn(f"{__tmp1.__class__.__name__}[{k!r}] = {v} ignored")
        return

    def __delitem__(__tmp1, v) :
        warnings.warn(f"del {__tmp1.__class__.__name__}[{v!r}] ignored")
        return

    def __len__(__tmp1) :
        return 0

    def __tmp8(__tmp1) :
        return iter([])


EmptyDict = EmptyDictType()
ExtraParams = NewType("ExtraParams", Dict[str, List[str]])
EmptyParams = cast("ExtraParams", EmptyDict)
ContextDict = NewType("ContextDict", Dict[Any, Any])  # defaultdict(lambda: None)
EmptyContext = cast("ContextDict", EmptyDict)


def copy_extra_params(__tmp5) :
    new: ExtraParams = ExtraParams(dict())
    if not __tmp5:
        return new
    for key, __tmp3 in __tmp5.items():
        if isinstance(__tmp3, str):
            new[key] = __tmp3
        elif isinstance(__tmp3, list):
            new[key] = list(__tmp3)
        else:
            raise ValueError(
                "can't convert extra param {} with value of type {}: {}".format(
                    key, type(__tmp3), __tmp3
                )
            )
    return new
