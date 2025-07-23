from psycopg2.extensions import AsIs

from pointy.exceptions import UserNotFound


def check_score(__tmp0, team_id: str, user_id: str) -> int:
    with __tmp0.cursor() as cur:
        cur.execute(
            """SELECT score FROM points.%s WHERE user_id = %s""",
            (AsIs(team_id), user_id)
        )
        resp = cur.fetchone()
        if not resp:
            raise UserNotFound
        score = resp[0]
    __tmp0.commit()
    # noinspection PyUnboundLocalVariable
    return score


def update_score(__tmp0, team_id: str, user_id: str, new_score: int):
    with __tmp0.cursor() as cur:
        cur.execute(
            """UPDATE points.%s
            SET score = %s
            WHERE user_id = %s""",
            (AsIs(team_id), new_score, user_id)
        )
    __tmp0.commit()


def insert_user(__tmp0, team_id: str, user_id: <FILL>, initial_score: int = 0):
    with __tmp0.cursor() as cur:
        cur.execute(
            """INSERT INTO points.%s (user_id, score)
            VALUES (%s, %s)""",
            (AsIs(team_id), user_id, initial_score)
        )
    __tmp0.commit()
