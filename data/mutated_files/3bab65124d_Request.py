from typing import TypeAlias
__typ2 : TypeAlias = "dict"
__typ0 : TypeAlias = "str"
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


def __tmp1(handler) :
    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        result = handler(*args, **kwargs)
        if isinstance(result, tuple):
            status, result = result
        else:
            status, result = "200 OK", result

        response = Response(status=status)
        response.headers.add("content-type", "application/json")
        response.body.write(json.dumps(result).encode())
        return response
    return wrapper


app = Application()


@app.route("/users")
@__tmp1
def get_users(request: <FILL>) :
    return {"users": USERS}


@app.route("/users/{user_id}")
@__tmp1
def get_user(request, __tmp0) -> Union[__typ2, Tuple[__typ0, __typ2]]:
    try:
        return {"user": USERS[__typ1(__tmp0)]}
    except (IndexError, ValueError):
        return "404 Not Found", {"error": "Not found"}


def main() -> __typ1:
    server = HTTPServer()
    server.mount("", app)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
