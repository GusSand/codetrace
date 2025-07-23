from protoactor.remote.response import ResponseStatusCode


class __typ0(Exception):
    def __init__(self, code: <FILL>, do_not_throw: bool = False):
        self.code = code
        self.do_not_throw = do_not_throw


class __typ1(__typ0):
    def __init__(self):
        super().__init__(int(ResponseStatusCode.Unavailable), True)