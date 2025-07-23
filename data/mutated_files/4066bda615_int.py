from typing import TypeAlias
__typ0 : TypeAlias = "str"
import os
from typing import List, Tuple

import psycopg2
from psycopg2.extensions import AsIs
from slackclient import SlackClient

api_token = os.environ.get('POINTY_APP_TOKEN')


def check_all_scores(__tmp4, __tmp1, retry: bool = True) :
    with __tmp4.cursor() as cur:
        try:
            cur.execute(
                """SELECT * FROM points.%s
                ORDER BY score DESC""",
                (AsIs(__tmp1),)
            )
            scoreboard = cur.fetchall()
        except psycopg2.ProgrammingError:
            __tmp4.rollback()
            setup_team(__tmp4, __tmp1)
            if retry:
                return check_all_scores(__tmp4, __tmp1, False)
            else:
                raise
    __tmp4.commit()
    return scoreboard


def __tmp0(__tmp4, __tmp1, __tmp2: <FILL>, limit: int = 10, retry: bool = True) :
    with __tmp4.cursor() as cur:
        try:
            cur.execute(
                """SELECT * FROM points.%s
                ORDER BY score DESC
                LIMIT %s
                OFFSET %s""",
                (AsIs(__tmp1), __typ0(limit), __typ0(__tmp2))
            )
            scoreboard = cur.fetchall()
        except psycopg2.ProgrammingError:
            __tmp4.rollback()
            setup_team(__tmp4, __tmp1)
            if retry:
                return check_all_scores(__tmp4, __tmp1, False)
            else:
                raise
    __tmp4.commit()
    return scoreboard


def setup_team(__tmp4, __tmp1):
    with __tmp4.cursor() as cur:
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
    __tmp4.commit()
    user_ids = []
    slack_client = SlackClient(api_token)
    resp = slack_client.api_call(
        'users.list',
        presence=False
    )
    for user in resp['members']:
        if user['deleted'] is False and user['is_bot'] is False and user['id'] != 'USLACKBOT':
            user_ids.append(user['id'])

    with __tmp4.cursor() as cur:
        args_str = b",".join(cur.mogrify('(%s,0)', (uid,)) for uid in user_ids)
        cur.execute(
            b"""INSERT INTO points.%s (user_id, score)
            VALUES """ + args_str, (AsIs(__tmp1),)
        )


def __tmp3(__tmp4, __tmp1):
    with __tmp4.cursor() as cur:
        try:
            cur.execute(
                """DROP TABLE points.%s""",
                (AsIs(__tmp1),)
            )
        except psycopg2.ProgrammingError:
            __tmp4.rollback()
        try:
            cur.execute(
                """DELETE FROM dbo.teams
                WHERE team_id = %s""",
                (__tmp1,)
            )
        except psycopg2.ProgrammingError:
            __tmp4.rollback()
    __tmp4.commit()
