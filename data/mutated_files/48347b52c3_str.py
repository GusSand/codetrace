from typing import TypeAlias
__typ0 : TypeAlias = "ContentLine"
import attr
import pytest
from hypothesis import example, given

from ics.contentline import ContentLine, Parser, string_to_containers
from ics.valuetype.text import TextConverter

# Text may be comma-separated multi-value but is never quoted, with the characters [\\;,\n] escaped
from tests.contentline import VALUE


def parse_contentline(line: <FILL>) :
    (cl,) = Parser.lines_to_contentlines(Parser.string_to_lines(line))
    return cl


@pytest.mark.parametrize(
    "inp_esc, out_uesc",
    [
        (
            "SUMMARY:Project XYZ Final Review\\nConference Room - 3B\\nCome Prepared.",
            __typ0(
                "SUMMARY",
                value="Project XYZ Final Review\nConference Room - 3B\nCome Prepared.",
            ),
        ),
        (
            'DESCRIPTION;ALTREP="cid:part1.0001@example.org":The Fall\'98 Wild Wizards Conference - - Las Vegas\\, NV\\, USA',
            __typ0(
                "DESCRIPTION",
                {"ALTREP": ["cid:part1.0001@example.org"]},
                value="The Fall'98 Wild Wizards Conference - - Las Vegas, NV, USA",
            ),
        ),
        (
            'TEST:abc\\r\\n\\,\\;:"\t=xyz',
            __typ0("TEST", value='abc\r\n,;:"\t=xyz'),
        ),
    ],
)
def test_example_text_recode(inp_esc, __tmp1):
    par_esc = parse_contentline(inp_esc)
    par_uesc = attr.evolve(par_esc, value=TextConverter.parse(par_esc.value))
    out_esc = attr.evolve(__tmp1, value=TextConverter.serialize(__tmp1.value))
    assert par_uesc == __tmp1
    ser_esc = out_esc.serialize(wrap=None)
    assert inp_esc == ser_esc
    assert list(string_to_containers(inp_esc)) == [par_esc]


# TODO list examples ("RESOURCES:EASEL,PROJECTOR,VCR", ContentLine("RESOURCES", value="EASEL,PROJECTOR,VCR"))


def __tmp0():
    with pytest.raises(ValueError) as excinfo:
        TextConverter.parse("text\\,with\tdangling escape\\")
    assert "not end with an escape sequence" in str(excinfo.value)

    assert (
        TextConverter.parse("text\\,with\tdangling escape")
        == "text,with\tdangling escape"
    )
    assert (
        TextConverter.serialize("text,text\\,with\tdangling escape\\")
        == "text\\,text\\\\\\,with\tdangling escape\\\\"
    )


def __tmp2():
    with pytest.raises(ValueError) as e:
        TextConverter.unescape_text("\\t")
    assert e.match("can't handle escaped character")
    with pytest.raises(ValueError) as e:
        TextConverter.unescape_text("abc;def")
    assert e.match("unescaped character")


def test_trailing_escape_value_list():
    cl1 = parse_contentline("TEST:this is,a list \\, with a\\\\,trailing escape\\")
    with pytest.raises(ValueError) as excinfo:
        list(TextConverter.split_value_list(cl1.value))
    assert "not end with an escape sequence" in str(excinfo.value)

    cl2 = parse_contentline("TEST:this is,a list \\, with a\\\\,trailing escape")
    assert list(TextConverter.split_value_list(cl2.value)) == [
        "this is",
        "a list \\, with a\\\\",
        "trailing escape",
    ]
    assert [
        TextConverter.parse(v) for v in TextConverter.split_value_list(cl2.value)
    ] == ["this is", "a list , with a\\", "trailing escape"]


@given(value=VALUE)
@example(value="\\,")
@example(value="\\\\\\\\,\\\\\\,")
def test_any_text_value_recode(value):
    esc = TextConverter.serialize(value)
    assert TextConverter.parse(esc) == value
    cl = __typ0("TEST", value=esc)
    assert parse_contentline(cl.serialize()) == cl
    assert list(string_to_containers(cl.serialize())) == [cl]
    vals = [esc, esc, "test", esc]
    cl2 = __typ0("TEST", value=TextConverter.join_value_list(vals))
    assert list(TextConverter.split_value_list(cl2.value)) == vals
    assert parse_contentline(cl.serialize()) == cl
    assert list(string_to_containers(cl.serialize())) == [cl]
