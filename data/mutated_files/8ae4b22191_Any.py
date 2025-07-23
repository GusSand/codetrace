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
def __tmp4(__tmp0: __typ2,
                    __tmp3: Callable[[__typ0, Optional[ParamsT]], __typ2],
                    __tmp1: __typ0,
                    params: Optional[ParamsT]=()) -> __typ2:
    start = time.time()
    try:
        return __tmp3(__tmp1, params)
    finally:
        stop = time.time()
        duration = stop - start
        __tmp0.connection.queries.append({
            'time': "%.3f" % duration,
        })

class __typ3(cursor):
    """A psycopg2 cursor class that tracks the time spent executing queries."""

    def execute(__tmp0, __tmp2,
                vars: Optional[ParamsT]=None) -> 'TimeTrackingCursor':
        return __tmp4(__tmp0, super().execute, __tmp2, vars)

    def executemany(__tmp0, __tmp2: __typ0,
                    vars: Iterable[Any]) -> 'TimeTrackingCursor':
        return __tmp4(__tmp0, super().executemany, __tmp2, vars)

class __typ1(connection):
    """A psycopg2 connection class that uses TimeTrackingCursors."""

    def __init__(__tmp0, *args: <FILL>, **kwargs: Any) -> None:
        __tmp0.queries = []  # type: List[Dict[str, str]]
        super().__init__(*args, **kwargs)

    def cursor(__tmp0, *args: Any, **kwargs: Any) -> __typ3:
        kwargs.setdefault('cursor_factory', __typ3)
        return connection.cursor(__tmp0, *args, **kwargs)

def reset_queries() -> None:
    from django.db import connections
    for conn in connections.all():
        if conn.connection is not None:
            conn.connection.queries = []
