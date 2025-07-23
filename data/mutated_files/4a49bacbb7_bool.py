from typing import TypeAlias
__typ0 : TypeAlias = "str"
import logging
from typing import Dict, List, Tuple

from werkzeug.datastructures import ImmutableMultiDict

from pointy.database.common import connect, channel_resp, ephemeral_resp
from pointy.database.team import check_scores, check_all_scores

logger = logging.getLogger(__name__)


def get_scoreboard_page(form: ImmutableMultiDict, __tmp0: int = None, limit: int = 10, ephemeral: bool = True) -> Dict[__typ0, __typ0]:
    logger.debug(f"Scoreboard request: offset {__tmp0}; limit {limit}; form: {form}")
    if 'command' in form:
        team_id = form['team_id']
        __tmp0 = __tmp0 if __tmp0 else 0
    else:
        team_id = form['team']['id']
        __tmp0 = __tmp0 if __tmp0 else int(form['actions'][0]['value'])

    with connect() as conn:
        # Try to fetch one more row. If limit + 1 rows come back, then there are more rows to display
        scoreboard_list = check_scores(conn, team_id, __tmp0=__tmp0, limit=limit+1)
    text, first, last = _parse_scoreboard(scoreboard_list, __tmp0=__tmp0, limit=limit)

    attachments = create_attachments(first, last, __tmp0, limit)
    return ephemeral_resp(text, attachments) if ephemeral else channel_resp(text, attachments)


def _parse_scoreboard(scoreboard_list, __tmp0: int, limit) :
    first = (__tmp0 == 0)
    # last is an indicator to whether there are more results to display
    last = not (len(scoreboard_list) > limit)
    if not last:
        # Then the last element of the scoreboard was just an indicator
        del(scoreboard_list[-1])

    text = f'Here\'s the points leaderboard:'
    for index, (subject, score) in enumerate(scoreboard_list):
        # offset+index+1 is the leaderboard position
        text += f'\n{__tmp0+index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0 and first:
            text += ' :crown:'
        elif index + 1 == len(scoreboard_list) and last:
            text += ' :hankey:'
    return text, first, last


def create_attachments(first: bool, last: <FILL>, __tmp0: int, limit: int):
    # Get the edge case out of the way:
    if first and last:
        return []
    actions = []
    if not first:
        actions.append({
                "name": "offset",
                "text": "Previous",
                "type": "button",
                "value": __tmp0 - limit
            })
    if not last:
        actions.append({
                "name": "offset",
                "text": "Next",
                "type": "button",
                "value": __tmp0 + limit
            })
    return [{
        "text": "",
        "fallback": "",
        "callback_id": "leader_scroll",
        "attachment_type": "default",
        "actions": actions
    }]


# depreciated
def get_scoreboard(form: ImmutableMultiDict, ephemeral: bool = True) -> Dict[__typ0, __typ0]:
    logger.debug(f"Scoreboard request: {form}")
    team_id = form.get('team_id', '')
    with connect() as conn:
        scoreboard_list = check_all_scores(conn, team_id)
    text = _parse_entire_scoreboard(scoreboard_list)
    return ephemeral_resp(text) if ephemeral else channel_resp(text)


# depreciated
def _parse_entire_scoreboard(scoreboard_list: List[Tuple[__typ0, int]]) -> __typ0:
    text = f'Here\'s a list of my favourite people:'
    for index, (subject, score) in enumerate(scoreboard_list):
        text += f'\n{index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0:
            text += ' :crown:'
        elif index + 1 == len(scoreboard_list):
            text += ' :hankey:'
    return text
