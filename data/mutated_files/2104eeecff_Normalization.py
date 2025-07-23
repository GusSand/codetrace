from typing import TypeAlias
__typ3 : TypeAlias = "NormalizationAction"
__typ2 : TypeAlias = "str"
__typ4 : TypeAlias = "tzinfo"
from datetime import tzinfo
from typing import ClassVar, Iterable, Iterator, List, Optional, Union, overload

import attr
from attr.validators import instance_of

from ics.component import Component
from ics.contentline import Container, lines_to_containers, string_to_containers
from ics.event import Event
from ics.timeline import Timeline
from ics.timespan import Normalization, NormalizationAction
from ics.todo import Todo


@attr.s
class __typ1(Component):
    version: __typ2 = attr.ib(
        validator=instance_of(__typ2), metadata={"ics_priority": 1000}
    )  # default set by Calendar.DEFAULT_VERSION
    prodid: __typ2 = attr.ib(
        validator=instance_of(__typ2), metadata={"ics_priority": 900}
    )  # default set by Calendar.DEFAULT_PRODID
    scale: Optional[__typ2] = attr.ib(default=None, metadata={"ics_priority": 800})
    method: Optional[__typ2] = attr.ib(default=None, metadata={"ics_priority": 700})
    # CalendarTimezoneConverter has priority 600

    events: List[Event] = attr.ib(
        factory=list, converter=list, metadata={"ics_priority": -100}
    )
    todos: List[Todo] = attr.ib(
        factory=list, converter=list, metadata={"ics_priority": -200}
    )


class __typ0(__typ1):
    """
    Represents a unique RFC 5545 iCalendar.

    Attributes:

        events: a list of `Event` contained in the Calendar
        todos: a list of `Todo` contained in the Calendar
        timeline: a `Timeline` instance for iterating this Calendar in chronological order

    """

    NAME = "VCALENDAR"
    DEFAULT_VERSION: ClassVar[__typ2] = "2.0"
    DEFAULT_PRODID: ClassVar[__typ2] = "ics.py 0.8.0.dev0 - http://git.io/lLljaA"

    def __init__(
        __tmp0,
        imports: Union[__typ2, Container, None] = None,
        events: Optional[Iterable[Event]] = None,
        todos: Optional[Iterable[Todo]] = None,
        __tmp4: __typ2 = None,
        **kwargs,
    ):
        """Initializes a new Calendar.

        Args:
            imports (**str**): data to be imported into the Calendar,
            events (**Iterable[Event]**): `Event` to be added to the calendar
            todos (**Iterable[Todo]**): `Todo` to be added to the calendar
            creator (**string**): uid of the creator program.
        """
        if events is None:
            events = tuple()
        if todos is None:
            todos = tuple()
        kwargs.setdefault("version", __tmp0.DEFAULT_VERSION)
        kwargs.setdefault(
            "prodid", __tmp4 if __tmp4 is not None else __tmp0.DEFAULT_PRODID
        )
        super().__init__(events=events, todos=todos, **kwargs)  # type: ignore[arg-type]
        __tmp0.timeline = Timeline(__tmp0, None)

        if imports is not None:
            if isinstance(imports, Container):
                __tmp0.populate(imports)
            else:
                if isinstance(imports, __typ2):
                    containers = iter(string_to_containers(imports))
                else:
                    containers = iter(lines_to_containers(imports))
                try:
                    container = next(containers)
                    if not isinstance(container, Container):
                        raise ValueError(f"can't populate from {type(container)}")
                    __tmp0.populate(container)
                except StopIteration:
                    raise ValueError("string didn't contain any ics data")
                try:
                    next(containers)
                    raise ValueError(
                        "Multiple calendars in one file are not supported by this method."
                        "Use ics.Calendar.parse_multiple()"
                    )
                except StopIteration:
                    pass

    @property
    def __tmp4(__tmp0) :
        return __tmp0.prodid

    @__tmp4.setter
    def __tmp4(__tmp0, __tmp1):
        __tmp0.prodid = __tmp1

    @classmethod
    def parse_multiple(__tmp3, string):
        """ "
        Parses an input string that may contain multiple calendars
        and returns a list of :class:`ics.event.Calendar`
        """
        containers = string_to_containers(string)
        return [__tmp3(imports=c) for c in containers]

    @overload
    def normalize(__tmp0, __tmp2: <FILL>):
        ...

    @overload
    def normalize(
        __tmp0,
        __tmp1: __typ4,
        __tmp7: __typ3,
        __tmp6,
    ):
        ...

    def normalize(__tmp0, __tmp2, *args, **kwargs):
        if isinstance(__tmp2, Normalization):
            if args or kwargs:
                raise ValueError(
                    "can't pass args or kwargs when a complete Normalization is given"
                )
        else:
            __tmp2 = Normalization(__tmp2, *args, **kwargs)
        __tmp0.events = [
            e if e.all_day else __tmp2.normalize(e) for e in __tmp0.events
        ]
        __tmp0.todos = [
            e if e.all_day else __tmp2.normalize(e) for e in __tmp0.todos
        ]

    def __tmp8(__tmp0) :
        return "<Calendar with {} event{} and {} todo{}>".format(
            len(__tmp0.events),
            "" if len(__tmp0.events) == 1 else "s",
            len(__tmp0.todos),
            "" if len(__tmp0.todos) == 1 else "s",
        )

    def __tmp5(__tmp0) :
        """Returns:
        iterable: an iterable version of __str__, line per line
        (with line-endings).

        Example:
            Can be used to write calendar to a file:

            >>> c = Calendar(); c.events.append(Event(summary="My cool event"))
            >>> open('my.ics', 'w').writelines(c)
        """
        return iter(__tmp0.serialize().splitlines(keepends=True))
