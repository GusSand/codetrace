from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
from io import BytesIO
from textwrap import dedent

import pytest

from scratch.request import Request


class StubSocket:
    def __tmp3(__tmp0, __tmp2: <FILL>):
        __tmp0._buff = BytesIO(__tmp2.encode())

    def __tmp5(__tmp0, n) :
        return __tmp0._buff.read(n)


def __tmp1(s: str) :
    return dedent(s).replace("\n", "\r\n")


@pytest.mark.parametrize("data,method,path,headers,body", [
    [
        __tmp1("""\
        GET / HTTP/1.0
        Accept: text/html

        """),

        "GET", "/", [("accept", "text/html")], b"",
    ],
    [
        __tmp1("""\
        POST /users HTTP/1.0
        Accept: application/json
        Content-type: application/json
        Content-length: 2

        {}"""),

        "POST",
        "/users",
        [
            ("accept", "application/json"),
            ("content-type", "application/json"),
            ("content-length", "2"),
        ],
        b"{}",
    ],
])
def __tmp4(__tmp2, method, path, headers, body):
    request = Request.from_socket(StubSocket(__tmp2))
    assert request.method == method
    assert request.path == path
    assert sorted(list(request.headers)) == sorted(headers)
    assert request.body.read(16384) == body


@pytest.mark.parametrize("data,error", [
    [
        "",
        ValueError("Request line missing."),
    ],

    [
        __tmp1("""\
        GET
        """),
        ValueError("Malformed request line 'GET'."),
    ],

    [
        __tmp1("""\
        GET / HTTP/1.0
        Content-type
        """),
        ValueError("Malformed header line b'Content-type'."),
    ],
])
def __tmp7(__tmp2, __tmp6):
    with pytest.raises(type(__tmp6)) as e:
        Request.from_socket(StubSocket(__tmp2))

    assert e.value.args == __tmp6.args
