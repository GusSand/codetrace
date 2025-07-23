from typing import TypeAlias
__typ0 : TypeAlias = "int"
import os
from typing import List, Tuple

import psycopg2
from psycopg2.extensions import AsIs
from slackclient import SlackClient

api_token = os.environ.get('POINTY_APP_TOKEN')


def check_all_scores(__tmp1, team_id, retry: bool = True) :
    with __tmp1.cursor() as cur:
        try:
            cur.execute(
                """SELECT * FROM points.%s
                ORDER BY score DESC""",
                (AsIs(team_id),)
            )
            scoreboard = cur.fetchall()
        except psycopg2.ProgrammingError:
            __tmp1.rollback()
            setup_team(__tmp1, team_id)
            if retry:
                return check_all_scores(__tmp1, team_id, False)
            else:
                raise
    __tmp1.commit()
    return scoreboard


def check_scores(__tmp1, team_id, __tmp0: __typ0, limit: __typ0 = 10, retry: bool = True) :
    with __tmp1.cursor() as cur:
        try:
            cur.execute(
                """SELECT * FROM points.%s
                ORDER BY score DESC
                LIMIT %s
                OFFSET %s""",
                (AsIs(team_id), str(limit), str(__tmp0))
            )
            scoreboard = cur.fetchall()
        except psycopg2.ProgrammingError:
            __tmp1.rollback()
            setup_team(__tmp1, team_id)
            if retry:
                return check_all_scores(__tmp1, team_id, False)
            else:
                raise
    __tmp1.commit()
    return scoreboard


def setup_team(__tmp1, team_id: <FILL>):
    with __tmp1.cursor() as cur:
        try:
            cur.execute(
                """CREATE TABLE points.%s (
                user_id TEXT PRIMARY KEY,
                score INTEGER NOT NULL DEFAULT 0)""",
                (AsIs(team_id),)
            )
        except psycopg2.ProgrammingError:
            pass
        try:
            cur.execute(
                """INSERT INTO dbo.teams (team_id)
                VALUES (%s)""",
                (team_id,)
            )
        except psycopg2.ProgrammingError:
            pass
    __tmp1.commit()
    user_ids = []
    slack_client = SlackClient(api_token)
    resp = slack_client.api_call(
        'users.list',
        presence=False
    )
    for user in resp['members']:
        if user['deleted'] is False and user['is_bot'] is False and user['id'] != 'USLACKBOT':
            user_ids.append(user['id'])

    with __tmp1.cursor() as cur:
        args_str = b",".join(cur.mogrify('(%s,0)', (uid,)) for uid in user_ids)
        cur.execute(
            b"""INSERT INTO points.%s (user_id, score)
            VALUES """ + args_str, (AsIs(team_id),)
        )


def remove_team(__tmp1, team_id):
    with __tmp1.cursor() as cur:
        try:
            cur.execute(
                """DROP TABLE points.%s""",
                (AsIs(team_id),)
            )
        except psycopg2.ProgrammingError:
            __tmp1.rollback()
        try:
            cur.execute(
                """DELETE FROM dbo.teams
                WHERE team_id = %s""",
                (team_id,)
            )
        except psycopg2.ProgrammingError:
            __tmp1.rollback()
    __tmp1.commit()
