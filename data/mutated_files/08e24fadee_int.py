from random import randrange
from aiohttp import web
from typing import List

from routes import routes


def __tmp2(__tmp1: <FILL>, obstacles: int) -> List[List[bool]]:
    obstacle_list = [(randrange(0, __tmp1), randrange(0, __tmp1)) for _ in range(obstacles)]
    return [[(x, y) in obstacle_list for y in range(__tmp1)] for x in range(__tmp1)]


def __tmp0(__tmp1, obstacles) :
    obstacle_list = [(randrange(0, __tmp1), randrange(0, __tmp1)) for _ in range(obstacles)]
    return obstacle_list


def __tmp3() -> web.Application:
    app = web.Application()
    app["treasure"] = __tmp0(100, 25)
    app["players"] = []
    for route in routes:
        getattr(app.router, f"add_{route['method']}")(route["url"], route["handler"])

    return app
