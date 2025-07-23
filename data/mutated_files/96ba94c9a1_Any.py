from typing import TypeAlias
__typ0 : TypeAlias = "NonBinaryStr"

import time
from psycopg2.extensions import cursor, connection

from typing import Callable, Optional, Iterable, Any, Dict, List, Union, TypeVar, \
    Mapping
from zerver.lib.str_utils import NonBinaryStr

__typ2 = TypeVar('CursorObj', bound=cursor)
ParamsT = Union[Iterable[Any], Mapping[str, Any]]

# Similar to the tracking done in Django's CursorDebugWrapper, but done at the
# psycopg2 cursor level so it works with SQLAlchemy.
def wrapper_execute(self,
                    action,
                    __tmp0,
                    params: Optional[ParamsT]=()) :
    start = time.time()
    try:
        return action(__tmp0, params)
    finally:
        stop = time.time()
        duration = stop - start
        self.connection.queries.append({
            'time': "%.3f" % duration,
        })

class __typ3(cursor):
    """A psycopg2 cursor class that tracks the time spent executing queries."""

    def execute(self, __tmp1,
                vars: Optional[ParamsT]=None) :
        return wrapper_execute(self, super().execute, __tmp1, vars)

    def executemany(self, __tmp1,
                    vars) :
        return wrapper_execute(self, super().executemany, __tmp1, vars)

class __typ1(connection):
    """A psycopg2 connection class that uses TimeTrackingCursors."""

    def __init__(self, *args, **kwargs) :
        self.queries = []  # type: List[Dict[str, str]]
        super().__init__(*args, **kwargs)

    def cursor(self, *args: <FILL>, **kwargs) :
        kwargs.setdefault('cursor_factory', __typ3)
        return connection.cursor(self, *args, **kwargs)

def reset_queries() :
    from django.db import connections
    for conn in connections.all():
        if conn.connection is not None:
            conn.connection.queries = []
