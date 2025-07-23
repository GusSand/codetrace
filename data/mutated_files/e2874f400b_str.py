from typing import TypeAlias
__typ0 : TypeAlias = "Request"
__typ1 : TypeAlias = "int"
import functools
import json
import sys
from typing import Callable, Tuple, Union

from .application import Application
from .request import Request
from .response import Response
from .server import HTTPServer

USERS = [
    {"id": 1, "name": "Jim"},
    {"id": 2, "name": "Bruce"},
    {"id": 3, "name": "Dick"},
]


def __tmp2(handler) :
    @functools.wraps(handler)
    def __tmp1(*args, **kwargs):
        result = handler(*args, **kwargs)
        if isinstance(result, tuple):
            status, result = result
        else:
            status, result = "200 OK", result

        response = Response(status=status)
        response.headers.add("content-type", "application/json")
        response.body.write(json.dumps(result).encode())
        return response
    return __tmp1


app = Application()


@app.route("/users")
@__tmp2
def get_users(request) :
    return {"users": USERS}


@app.route("/users/{user_id}")
@__tmp2
def __tmp0(request: __typ0, user_id: <FILL>) :
    try:
        return {"user": USERS[__typ1(user_id)]}
    except (IndexError, ValueError):
        return "404 Not Found", {"error": "Not found"}


def main() :
    server = HTTPServer()
    server.mount("", app)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
