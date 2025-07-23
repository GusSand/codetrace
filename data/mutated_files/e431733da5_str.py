from django.db.models.query import QuerySet
from psycopg2.extensions import cursor
from typing import Any, Callable, Dict, List, Tuple, TypeVar

import re
import time

CursorObj = TypeVar('CursorObj', bound=cursor)

def create_index_if_not_exist(__tmp1, __tmp5, __tmp0: <FILL>,
                              __tmp6: str) -> str:
    #
    # FUTURE TODO: When we no longer need to support postgres 9.3 for Trusty,
    #              we can use "IF NOT EXISTS", which is part of postgres 9.5
    #              (and which already is supported on Xenial systems).
    stmt = '''
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_class
                where relname = '%s'
                ) THEN
                    CREATE INDEX
                    %s
                    ON %s (%s)
                    %s;
            END IF;
        END$$;
        ''' % (__tmp1, __tmp1, __tmp5, __tmp0, __tmp6)
    return stmt


def __tmp7(cursor,
                    __tmp2,
                    __tmp4,
                    __tmp3: List[str],
                    batch_size: int=10000,
                    sleep: float=0.1,
                    escape: bool=True) -> None:  # nocoverage
    stmt = '''
        UPDATE %s
        SET (%s) = (%s)
        WHERE id >= %%s AND id < %%s
    ''' % (__tmp2, ', '.join(__tmp4), ', '.join(['%s'] * len(__tmp4)))

    cursor.execute("SELECT MIN(id), MAX(id) FROM %s" % (__tmp2,))
    (min_id, max_id) = cursor.fetchall()[0]
    if min_id is None:
        return

    print("\n    Range of rows to update: [%s, %s]" % (min_id, max_id))
    while min_id <= max_id:
        lower = min_id
        upper = min_id + batch_size
        print('    Updating range [%s,%s)' % (lower, upper))
        params = list(__tmp3) + [lower, upper]
        if escape:
            cursor.execute(stmt, params=params)
        else:
            cursor.execute(stmt % tuple(params))

        min_id = upper
        time.sleep(sleep)

        # Once we've finished, check if any new rows were inserted to the table
        if min_id > max_id:
            cursor.execute("SELECT MAX(id) FROM %s" % (__tmp2,))
            max_id = cursor.fetchall()[0][0]

    print("    Finishing...", end='')
