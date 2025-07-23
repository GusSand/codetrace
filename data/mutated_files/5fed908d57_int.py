from random import randrange
from aiohttp import web
from typing import List

from routes import routes


def generate_grid(size, __tmp1: int) :
    obstacle_list = [(randrange(0, size), randrange(0, size)) for _ in range(__tmp1)]
    return [[(x, y) in obstacle_list for y in range(size)] for x in range(size)]


def __tmp0(size: <FILL>, __tmp1: int) -> List[List[bool]]:
    obstacle_list = [(randrange(0, size), randrange(0, size)) for _ in range(__tmp1)]
    return obstacle_list


def create_app() -> web.Application:
    app = web.Application()
    app["treasure"] = __tmp0(100, 25)
    app["players"] = []
    for route in routes:
        getattr(app.router, f"add_{route['method']}")(route["url"], route["handler"])

    return app
