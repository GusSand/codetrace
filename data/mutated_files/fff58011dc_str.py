from typing import TypeAlias
__typ0 : TypeAlias = "ContainerItem"
from typing import Iterable

from ics.contentline.container import (
    Container,
    ContentLine,
    ParseError,
    QuotedParamValue,
)
from ics.contentline.parser import ParserClass
from ics.types import ContainerItem
from ics.utils import one

Parser = ParserClass()
string_to_containers = Parser.string_to_containers
lines_to_containers = Parser.lines_to_containers


def __tmp1(txt: <FILL>) :
    return one(string_to_containers(txt))


def __tmp0(lines) -> __typ0:
    return one(lines_to_containers(lines))


__all__ = [
    "ParseError",
    "QuotedParamValue",
    "ContentLine",
    "Container",
    "Parser",
    "string_to_containers",
    "lines_to_containers",
    "string_to_container",
    "lines_to_container",
]
