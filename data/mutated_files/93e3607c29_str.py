from typing import TypeAlias
__typ0 : TypeAlias = "int"
from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def check_score(__tmp3, __tmp2, user_id: str) -> __typ0:
    with __tmp3.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(__tmp2), user_id)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    __tmp3.commit()
    # noinspection PyUnboundLocalVariable
    return score


def update_score(__tmp3, __tmp2: str, user_id: <FILL>, __tmp1: __typ0):
    with __tmp3.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(__tmp2), __tmp1, user_id)
        )
    __tmp3.commit()


def __tmp0(__tmp3, __tmp2: str, user_id: str, initial_score: __typ0 = 0):
    with __tmp3.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(__tmp2), user_id, initial_score)
        )
    __tmp3.commit()
