import re
import warnings
from typing import Iterable, Iterator, Type

from ics.types import ContextDict, EmptyContext, EmptyParams, ExtraParams
from ics.utils import next_after_str_escape
from ics.valuetype.base import ValueConverter

__all__ = ["TextConverter", "RawTextConverter"]


class RawTextConverterClass(ValueConverter[str]):
    @property
    def ics_type(__tmp0) :
        return "RAWTEXT"

    @property
    def __tmp4(__tmp0) -> Type[str]:
        return str

    def parse(
        __tmp0,
        value: str,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return value

    def serialize(
        __tmp0,
        value: <FILL>,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return value


RawTextConverter = RawTextConverterClass()


class TextConverterClass(ValueConverter[str]):
    @property
    def ics_type(__tmp0) :
        return "TEXT"

    @property
    def __tmp4(__tmp0) :
        return str

    def parse(
        __tmp0,
        value: str,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return __tmp0.unescape_text(value)

    def serialize(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return __tmp0.escape_text(value)

    def __tmp1(__tmp0, values: str) -> Iterable[str]:
        it = iter(values.split(","))
        for val in it:
            while True:
                m = re.search(r"\\+$", val)  # find any trailing backslash
                if m and (m.end() - m.start()) % 2 == 1:
                    # odd number of trailing backslashes => comma was escaped, include next segment
                    val += "," + next_after_str_escape(it, full_str=values)
                else:
                    break
            yield val

    def join_value_list(__tmp0, values) :
        def __tmp3():
            for value in values:
                m = re.search(r"\\[;,]|" + "[\n\r]", value)
                if m:
                    warnings.warn(f"TEXT value in list may not contain {m}: {value}")
                yield value

        return ",".join(__tmp3())

    @classmethod
    def escape_text(__tmp2, string: str) :
        return string.translate(
            {
                ord("\\"): "\\\\",
                ord(";"): "\\;",
                ord(","): "\\,",
                ord("\n"): "\\n",
                ord("\r"): "\\r",
            }
        )

    @classmethod
    def unescape_text(__tmp2, string: str) :
        return "".join(__tmp2.unescape_text_iter(string))

    @classmethod
    def unescape_text_iter(__tmp2, string: str) :
        it = iter(string)
        for c1 in it:
            if c1 == "\\":
                c2 = next_after_str_escape(it, full_str=string)
                if c2 == ";":
                    yield ";"
                elif c2 == ",":
                    yield ","
                elif c2 == "n" or c2 == "N":
                    yield "\n"
                elif c2 == "r" or c2 == "R":
                    yield "\r"
                elif c2 == "\\":
                    yield "\\"
                else:
                    raise ValueError(f"can't handle escaped character '{c2}'")
            elif c1 in ";,\n\r":
                raise ValueError(f"unescaped character '{c1}' in TEXT value")
            else:
                yield c1


TextConverter = TextConverterClass()
ValueConverter.BY_TYPE[str] = TextConverter
