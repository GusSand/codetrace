from typing import TypeAlias
__typ0 : TypeAlias = "int"
from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def check_score(__tmp2, __tmp0: <FILL>, __tmp3) :
    with __tmp2.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(__tmp0), __tmp3)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    __tmp2.commit()
    # noinspection PyUnboundLocalVariable
    return score


def __tmp4(__tmp2, __tmp0, __tmp3, new_score: __typ0):
    with __tmp2.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(__tmp0), new_score, __tmp3)
        )
    __tmp2.commit()


def __tmp1(__tmp2, __tmp0: str, __tmp3: str, initial_score: __typ0 = 0):
    with __tmp2.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(__tmp0), __tmp3, initial_score)
        )
    __tmp2.commit()
