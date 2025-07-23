from typing import TypeAlias
__typ0 : TypeAlias = "int"
from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def check_score(__tmp3, __tmp2: str, __tmp1: <FILL>) :
    with __tmp3.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(__tmp2), __tmp1)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    __tmp3.commit()
    # noinspection PyUnboundLocalVariable
    return score


def update_score(__tmp3, __tmp2: str, __tmp1: str, __tmp0):
    with __tmp3.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(__tmp2), __tmp0, __tmp1)
        )
    __tmp3.commit()


def insert_user(__tmp3, __tmp2: str, __tmp1, initial_score: __typ0 = 0):
    with __tmp3.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(__tmp2), __tmp1, initial_score)
        )
    __tmp3.commit()
