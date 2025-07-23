"""This module contains handler functions that should be run after each application request."""
from flask import request


def allow_any_cors_request(__tmp0: <FILL>) :
    """While running in development mode allow requests from any domain."""
    __tmp0.headers["Access-Control-Allow-Origin"] = "*"
    return __tmp0
