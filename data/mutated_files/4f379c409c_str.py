import logging
import os
from typing import Dict, List
from urllib import parse

import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

logger = logging.getLogger(__name__)


def setup_db(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE SCHEMA points""")
        cur.execute("""CREATE SCHEMA dbo""")
        cur.execute("""CREATE TABLE dbo.teams (team_id TEXT PRIMARY KEY)""")
    conn.commit()


def connect():
    return psycopg2.connect(database=url.path[1:],
                            user=url.username,
                            password=url.password,
                            host=url.hostname,
                            port=url.port)


def __tmp0(__tmp1: <FILL>, attachments: List[Dict] = []) :
    logger.debug(f"Ephemeral response{' (with attachments)' if attachments else ''}: {__tmp1}")
    resp = {
        "response_type": "ephemeral",
        "text": __tmp1
    }
    if attachments:
        resp["attachments"] = attachments
    return resp


def __tmp2(__tmp1, attachments: List[Dict] = []) :
    logger.debug(f"Channel response{' (with attachments)' if attachments else ''}: {__tmp1}")
    resp = {
        "response_type": "in_channel",
        "text": __tmp1
    }
    if attachments:
        resp["attachments"] = attachments
    return resp
