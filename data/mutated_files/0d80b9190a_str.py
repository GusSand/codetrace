import re
import warnings
from typing import Iterable, Iterator, Type

from ics.types import ContextDict, EmptyContext, EmptyParams, ExtraParams
from ics.utils import next_after_str_escape
from ics.valuetype.base import ValueConverter

__all__ = ["TextConverter", "RawTextConverter"]


class RawTextConverterClass(ValueConverter[str]):
    @property
    def __tmp4(__tmp0) -> str:
        return "RAWTEXT"

    @property
    def python_type(__tmp0) :
        return str

    def parse(
        __tmp0,
        value: str,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return value

    def __tmp6(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) -> str:
        return value


RawTextConverter = RawTextConverterClass()


class __typ0(ValueConverter[str]):
    @property
    def __tmp4(__tmp0) :
        return "TEXT"

    @property
    def python_type(__tmp0) :
        return str

    def parse(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return __tmp0.unescape_text(value)

    def __tmp6(
        __tmp0,
        value,
        params: ExtraParams = EmptyParams,
        context: ContextDict = EmptyContext,
    ) :
        return __tmp0.escape_text(value)

    def split_value_list(__tmp0, __tmp5) -> Iterable[str]:
        it = iter(__tmp5.split(","))
        for val in it:
            while True:
                m = re.search(r"\\+$", val)  # find any trailing backslash
                if m and (m.end() - m.start()) % 2 == 1:
                    # odd number of trailing backslashes => comma was escaped, include next segment
                    val += "," + next_after_str_escape(it, full_str=__tmp5)
                else:
                    break
            yield val

    def __tmp2(__tmp0, __tmp5: Iterable[str]) :
        def __tmp3():
            for value in __tmp5:
                m = re.search(r"\\[;,]|" + "[\n\r]", value)
                if m:
                    warnings.warn(f"TEXT value in list may not contain {m}: {value}")
                yield value

        return ",".join(__tmp3())

    @classmethod
    def escape_text(__tmp1, string: <FILL>) :
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
    def unescape_text(__tmp1, string) :
        return "".join(__tmp1.unescape_text_iter(string))

    @classmethod
    def unescape_text_iter(__tmp1, string) :
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


TextConverter = __typ0()
ValueConverter.BY_TYPE[str] = TextConverter
