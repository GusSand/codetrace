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
    def __tmp8(cls, instance):
        return isinstance(instance, timedelta)


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
CalendarEntryOrTimespan = Union["CalendarEntryAttrs", "Timespan"]
CalendarEntryOrTimespanOrInstant = Union["CalendarEntryAttrs", "Timespan", datetime]


@overload
def __tmp4(__tmp2) -> "Timespan":
    ...


@overload
def __tmp4(__tmp2: datetime) :
    ...


@overload
def __tmp4(__tmp2) :
    ...


def __tmp4(__tmp2):
    from ics.event import (  # noqa: F811 # pyflakes considers this a redef of the unused if TYPE_CHECKING import above
        CalendarEntryAttrs,
    )

    if isinstance(__tmp2, CalendarEntryAttrs):
        return __tmp2.timespan
    else:
        return __tmp2


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

    def __tmp5(__tmp0):
        object.__setattr__(__tmp0, "__post_init__", True)

    def __setattr__(__tmp0, key, __tmp2):
        if getattr(__tmp0, "__post_init__", None):
            cls = __tmp0.__class__  # type: Any
            if not getattr(cls, "__attr_fields__", None):
                cls.__attr_fields__ = attr.fields_dict(cls)
            try:
                field = cls.__attr_fields__[key]
            except KeyError:
                pass
            else:  # when no KeyError was thrown
                if field.converter is not None:
                    __tmp2 = field.converter(__tmp2)
                if field.validator is not None:
                    field.validator(__tmp0, field, __tmp2)
        super().__setattr__(key, __tmp2)


class EmptyDictType(MutableMapping[Any, None]):
    """An empty, immutable dict that returns `None` for any key. Useful as default value for function arguments."""

    def __getitem__(__tmp0, k: Any) :
        return None

    def __tmp1(__tmp0, k, v: <FILL>) :
        warnings.warn(f"{__tmp0.__class__.__name__}[{k!r}] = {v} ignored")
        return

    def __tmp7(__tmp0, v: Any) -> None:
        warnings.warn(f"del {__tmp0.__class__.__name__}[{v!r}] ignored")
        return

    def __len__(__tmp0) -> int:
        return 0

    def __tmp6(__tmp0) :
        return iter([])


EmptyDict = EmptyDictType()
ExtraParams = NewType("ExtraParams", Dict[str, List[str]])
EmptyParams = cast("ExtraParams", EmptyDict)
ContextDict = NewType("ContextDict", Dict[Any, Any])  # defaultdict(lambda: None)
EmptyContext = cast("ContextDict", EmptyDict)


def copy_extra_params(__tmp3: Optional[ExtraParams]) -> ExtraParams:
    new: ExtraParams = ExtraParams(dict())
    if not __tmp3:
        return new
    for key, __tmp2 in __tmp3.items():
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
