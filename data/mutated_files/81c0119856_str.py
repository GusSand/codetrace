from typing import TypeAlias
__typ0 : TypeAlias = "ImmutableMultiDict"
import logging
import re
from typing import Tuple, Dict

from werkzeug.datastructures import ImmutableMultiDict

from pointy.database.common import connect, ephemeral_resp, channel_resp
from pointy.database.user import check_score, update_score
from pointy.exceptions import AddPointsError, UserNotFound

logger = logging.getLogger(__name__)

MAX_SCORE_ADD = 20

add_points_re = re.compile("^<@[A-Z][a-zA-Z0-9]+(\|[^>]*)?> -?[0-9]+( .*)?$")


def __tmp1(__tmp2: __typ0) :
    logger.debug(f"Add points request: {__tmp2}")
    __tmp3 = __tmp2.get('text', '')
    try:
        subject_id, points, reason = __tmp0(__tmp3)
    except AddPointsError:
        return ephemeral_resp("Sorry, I don't understand that!")
    pointer = __tmp2.get('user_id')
    if pointer and subject_id == pointer:
        return ephemeral_resp("Cheeky, you can't give yourself points!")
    if abs(points) > MAX_SCORE_ADD:
        return ephemeral_resp(f"Your team only allows adding {MAX_SCORE_ADD} points at once")
    team_id = __tmp2.get('team_id', '')
    with connect() as conn:
        try:
            current_score = check_score(conn, team_id, subject_id)
        except UserNotFound:
            return ephemeral_resp("User not found.")
        new_score = current_score + points
        update_score(conn, team_id, subject_id, new_score)
        return channel_resp(f"<@{subject_id}>: {current_score} -> {new_score} {reason}")


def __tmp0(__tmp3: <FILL>) -> Tuple[str, int, str]:
    if not add_points_re.match(__tmp3):
        raise AddPointsError(__tmp3)
    ltatidentity = __tmp3.split('>')[0]
    pointreason = '>'.join(__tmp3.split('>')[1:])
    points = int(pointreason[1:].split(' ')[0])
    reason = ' '.join(pointreason[1:].split(' ')[1:])
    identity = ltatidentity[2:]
    user_id, display_name = identity.split('|')
    return user_id, points, reason
