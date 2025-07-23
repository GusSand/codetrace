from typing import TypeAlias
__typ0 : TypeAlias = "str"
from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def check_score(__tmp2, __tmp1, user_id) :
    with __tmp2.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(__tmp1), user_id)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    __tmp2.commit()
    # noinspection PyUnboundLocalVariable
    return score


def update_score(__tmp2, __tmp1, user_id: __typ0, new_score: <FILL>):
    with __tmp2.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(__tmp1), new_score, user_id)
        )
    __tmp2.commit()


def __tmp0(__tmp2, __tmp1: __typ0, user_id: __typ0, initial_score: int = 0):
    with __tmp2.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(__tmp1), user_id, initial_score)
        )
    __tmp2.commit()
