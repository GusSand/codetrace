from typing import TypeAlias
__typ0 : TypeAlias = "int"
import os
from typing import List, Tuple

import psycopg2
from psycopg2.extensions import AsIs
from slackclient import SlackClient

api_token = os.environ.get('POINTY_APP_TOKEN')


def __tmp2(__tmp6, __tmp1: <FILL>, retry: bool = True) :
    with __tmp6.cursor() as cur:
        try:
            cur.execute(
                """SELECT * FROM points.%s
                ORDER BY score DESC""",
                (AsIs(__tmp1),)
            )
            scoreboard = cur.fetchall()
        except psycopg2.ProgrammingError:
            __tmp6.rollback()
            __tmp3(__tmp6, __tmp1)
            if retry:
                return __tmp2(__tmp6, __tmp1, False)
            else:
                raise
    __tmp6.commit()
    return scoreboard


def __tmp0(__tmp6, __tmp1, __tmp4: __typ0, limit: __typ0 = 10, retry: bool = True) -> List[Tuple[str, __typ0]]:
    with __tmp6.cursor() as cur:
        try:
            cur.execute(
                """SELECT * FROM points.%s
                ORDER BY score DESC
                LIMIT %s
                OFFSET %s""",
                (AsIs(__tmp1), str(limit), str(__tmp4))
            )
            scoreboard = cur.fetchall()
        except psycopg2.ProgrammingError:
            __tmp6.rollback()
            __tmp3(__tmp6, __tmp1)
            if retry:
                return __tmp2(__tmp6, __tmp1, False)
            else:
                raise
    __tmp6.commit()
    return scoreboard


def __tmp3(__tmp6, __tmp1: str):
    with __tmp6.cursor() as cur:
        try:
            cur.execute(
                """CREATE TABLE points.%s (
                user_id TEXT PRIMARY KEY,
                score INTEGER NOT NULL DEFAULT 0)""",
                (AsIs(__tmp1),)
            )
        except psycopg2.ProgrammingError:
            pass
        try:
            cur.execute(
                """INSERT INTO dbo.teams (team_id)
                VALUES (%s)""",
                (__tmp1,)
            )
        except psycopg2.ProgrammingError:
            pass
    __tmp6.commit()
    user_ids = []
    slack_client = SlackClient(api_token)
    resp = slack_client.api_call(
        'users.list',
        presence=False
    )
    for user in resp['members']:
        if user['deleted'] is False and user['is_bot'] is False and user['id'] != 'USLACKBOT':
            user_ids.append(user['id'])

    with __tmp6.cursor() as cur:
        args_str = b",".join(cur.mogrify('(%s,0)', (uid,)) for uid in user_ids)
        cur.execute(
            b"""INSERT INTO points.%s (user_id, score)
            VALUES """ + args_str, (AsIs(__tmp1),)
        )


def __tmp5(__tmp6, __tmp1: str):
    with __tmp6.cursor() as cur:
        try:
            cur.execute(
                """DROP TABLE points.%s""",
                (AsIs(__tmp1),)
            )
        except psycopg2.ProgrammingError:
            __tmp6.rollback()
        try:
            cur.execute(
                """DELETE FROM dbo.teams
                WHERE team_id = %s""",
                (__tmp1,)
            )
        except psycopg2.ProgrammingError:
            __tmp6.rollback()
    __tmp6.commit()
