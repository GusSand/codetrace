from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def __tmp4(__tmp5, __tmp0: str, __tmp3) -> int:
    with __tmp5.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(__tmp0), __tmp3)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    __tmp5.commit()
    # noinspection PyUnboundLocalVariable
    return score


def update_score(__tmp5, __tmp0: str, __tmp3: str, __tmp2: int):
    with __tmp5.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(__tmp0), __tmp2, __tmp3)
        )
    __tmp5.commit()


def __tmp1(__tmp5, __tmp0: <FILL>, __tmp3: str, initial_score: int = 0):
    with __tmp5.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(__tmp0), __tmp3, initial_score)
        )
    __tmp5.commit()
