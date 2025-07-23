import werkzeug.exceptions


class BadRequest(werkzeug.exceptions.BadRequest):
    def __init__(__tmp1, type: str, __tmp0) :
        super().__init__(__tmp0)
        __tmp1.type = type


class NotFound(werkzeug.exceptions.NotFound):
    def __init__(__tmp1, type: <FILL>, __tmp0: str) -> None:
        super().__init__(__tmp0)
        __tmp1.type = type


class Unauthorized(werkzeug.exceptions.Unauthorized):
    def __init__(__tmp1, type, __tmp0) :
        super().__init__(__tmp0)
        __tmp1.type = type
