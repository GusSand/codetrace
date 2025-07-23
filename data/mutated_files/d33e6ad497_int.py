from typing import TypeAlias
__typ0 : TypeAlias = "str"
from io import BytesIO
from textwrap import dedent

import pytest

from scratch.request import Request


class StubSocket:
    def __init__(__tmp0, data):
        __tmp0._buff = BytesIO(data.encode())

    def recv(__tmp0, n: <FILL>) -> bytes:
        return __tmp0._buff.read(n)


def __tmp1(s) -> __typ0:
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
def test_requests(data, method, path, headers, body):
    request = Request.from_socket(StubSocket(data))
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
def test_invalid_requests(data, error):
    with pytest.raises(type(error)) as e:
        Request.from_socket(StubSocket(data))

    assert e.value.args == error.args
