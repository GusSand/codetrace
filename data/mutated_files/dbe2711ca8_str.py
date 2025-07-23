from typing import TypeAlias
__typ0 : TypeAlias = "int"
from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def __tmp3(conn, __tmp0, __tmp2: str) -> __typ0:
    with conn.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(__tmp0), __tmp2)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    conn.commit()
    # noinspection PyUnboundLocalVariable
    return score


def __tmp4(conn, __tmp0: <FILL>, __tmp2: str, __tmp1: __typ0):
    with conn.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(__tmp0), __tmp1, __tmp2)
        )
    conn.commit()


def insert_user(conn, __tmp0: str, __tmp2, initial_score: __typ0 = 0):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(__tmp0), __tmp2, initial_score)
        )
    conn.commit()
