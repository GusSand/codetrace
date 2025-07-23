
import time
from psycopg2.extensions import cursor, connection

from typing import Callable, Optional, Iterable, Any, Dict, List, Union, TypeVar, \
    Mapping
from zerver.lib.str_utils import NonBinaryStr

__typ0 = TypeVar('CursorObj', bound=cursor)
ParamsT = Union[Iterable[Any], Mapping[str, Any]]

# Similar to the tracking done in Django's CursorDebugWrapper, but done at the
# psycopg2 cursor level so it works with SQLAlchemy.
def __tmp3(__tmp2: __typ0,
                    action,
                    sql: NonBinaryStr,
                    params: Optional[ParamsT]=()) -> __typ0:
    start = time.time()
    try:
        return action(sql, params)
    finally:
        stop = time.time()
        duration = stop - start
        __tmp2.connection.queries.append({
            'time': "%.3f" % duration,
        })

class TimeTrackingCursor(cursor):
    """A psycopg2 cursor class that tracks the time spent executing queries."""

    def execute(__tmp2, __tmp0: NonBinaryStr,
                vars: Optional[ParamsT]=None) -> 'TimeTrackingCursor':
        return __tmp3(__tmp2, super().execute, __tmp0, vars)

    def executemany(__tmp2, __tmp0,
                    vars: Iterable[Any]) -> 'TimeTrackingCursor':
        return __tmp3(__tmp2, super().executemany, __tmp0, vars)

class TimeTrackingConnection(connection):
    """A psycopg2 connection class that uses TimeTrackingCursors."""

    def __init__(__tmp2, *args: Any, **kwargs: <FILL>) :
        __tmp2.queries = []  # type: List[Dict[str, str]]
        super().__init__(*args, **kwargs)

    def cursor(__tmp2, *args: Any, **kwargs) -> TimeTrackingCursor:
        kwargs.setdefault('cursor_factory', TimeTrackingCursor)
        return connection.cursor(__tmp2, *args, **kwargs)

def __tmp1() -> None:
    from django.db import connections
    for conn in connections.all():
        if conn.connection is not None:
            conn.connection.queries = []
