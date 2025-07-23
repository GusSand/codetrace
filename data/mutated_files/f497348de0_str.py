from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
__typ2 : TypeAlias = "Headers"
import typing
from io import BytesIO
from textwrap import dedent

import pytest

from scratch.headers import Headers
from scratch.response import Response


class __typ0:
    def __tmp5(__tmp0) -> None:
        __tmp0._buff = BytesIO()

    def __tmp7(__tmp0, __tmp2: __typ1) -> None:
        __tmp0._buff.write(__tmp2)

    def __tmp3(__tmp0, f: typing.IO[__typ1]) -> None:
        __tmp0._buff.write(f.read())

    def getvalue(__tmp0) -> __typ1:
        return __tmp0._buff.getvalue()


def make_output(s: <FILL>) -> str:
    return dedent(s).replace("\n", "\r\n").encode()


def __tmp4(*headers) :
    res = __typ2()
    for name, value in headers:
        res.add(name, value)
    return res


@pytest.mark.parametrize("response,output", [
    [
        Response("200 OK"),
        make_output("""\
        HTTP/1.1 200 OK

        """)
    ],

    [
        Response("200 OK", headers=__tmp4(
            ("content-type", "application/json"),
            ("content-length", "2"),
        ), content="{}"),
        make_output("""\
        HTTP/1.1 200 OK
        content-type: application/json
        content-length: 2

        {}""")
    ],

    [
        Response("200 OK", headers=__tmp4(
            ("content-type", "text/html"),
            ("content-length", "5"),
        ), body=BytesIO(b"Hello")),
        make_output("""\
        HTTP/1.1 200 OK
        content-type: text/html
        content-length: 5

        Hello""")
    ],

    [
        Response(
            "200 OK",
            headers=__tmp4(("content-type", "text/plain")),
            body=open("tests/fixtures/plain", "rb")
        ),
        make_output("""\
        HTTP/1.1 200 OK
        content-type: text/plain
        content-length: 5

        Hello""")
    ]
])
def __tmp6(response, __tmp1):
    socket = __typ0()
    response.send(socket)
    assert socket.getvalue() == __tmp1
