import logging
import re
from typing import Dict

from werkzeug.datastructures import ImmutableMultiDict

from pointy.database.common import connect, ephemeral_resp, channel_resp
from pointy.database.user import check_score
from pointy.exceptions import GetScoreError, UserNotFound

logger = logging.getLogger(__name__)

check_score_re = re.compile("^<@[A-Z][a-zA-Z0-9]+(\|[^>]*)?> ?$")


def __tmp2(__tmp0) :
    logger.debug(f"Get score request: {__tmp0}")
    __tmp1 = __tmp0.get('text', '')
    try:
        subject_id = parse_get_score(__tmp1)
    except GetScoreError:
        return ephemeral_resp(f"Could not parse {__tmp1}")
    team_id = __tmp0.get('team_id', '')
    with connect() as conn:
        try:
            score = check_score(conn, team_id, subject_id)
        except UserNotFound:
            return ephemeral_resp(f"User not found")  # TODO add them if they're a user?
        return channel_resp(f"{__tmp1.strip()} has {score} point{'s' if score != 1 else ''}")


def parse_get_score(__tmp1: <FILL>) :
    if not check_score_re.match(__tmp1):
        raise GetScoreError(__tmp1)
    user_id, display_name = __tmp1.strip()[2:-1].split('|')
    return user_id
