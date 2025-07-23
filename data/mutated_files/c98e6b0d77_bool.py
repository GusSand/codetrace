from typing import TypeAlias
__typ0 : TypeAlias = "ImmutableMultiDict"
__typ1 : TypeAlias = "int"
import logging
from typing import Dict, List, Tuple

from werkzeug.datastructures import ImmutableMultiDict

from pointy.database.common import connect, channel_resp, ephemeral_resp
from pointy.database.team import check_scores, check_all_scores

logger = logging.getLogger(__name__)


def __tmp4(__tmp0: __typ0, __tmp6: __typ1 = None, __tmp2: __typ1 = 10, ephemeral: bool = True) :
    logger.debug(f"Scoreboard request: offset {__tmp6}; limit {__tmp2}; form: {__tmp0}")
    if 'command' in __tmp0:
        team_id = __tmp0['team_id']
        __tmp6 = __tmp6 if __tmp6 else 0
    else:
        team_id = __tmp0['team']['id']
        __tmp6 = __tmp6 if __tmp6 else __typ1(__tmp0['actions'][0]['value'])

    with connect() as conn:
        # Try to fetch one more row. If limit + 1 rows come back, then there are more rows to display
        __tmp3 = check_scores(conn, team_id, __tmp6=__tmp6, __tmp2=__tmp2+1)
    text, first, last = __tmp1(__tmp3, __tmp6=__tmp6, __tmp2=__tmp2)

    attachments = create_attachments(first, last, __tmp6, __tmp2)
    return ephemeral_resp(text, attachments) if ephemeral else channel_resp(text, attachments)


def __tmp1(__tmp3, __tmp6: __typ1, __tmp2: __typ1) :
    first = (__tmp6 == 0)
    # last is an indicator to whether there are more results to display
    last = not (len(__tmp3) > __tmp2)
    if not last:
        # Then the last element of the scoreboard was just an indicator
        del(__tmp3[-1])

    text = f'Here\'s the points leaderboard:'
    for index, (subject, score) in enumerate(__tmp3):
        # offset+index+1 is the leaderboard position
        text += f'\n{__tmp6+index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0 and first:
            text += ' :crown:'
        elif index + 1 == len(__tmp3) and last:
            text += ' :hankey:'
    return text, first, last


def create_attachments(first: <FILL>, last, __tmp6: __typ1, __tmp2):
    # Get the edge case out of the way:
    if first and last:
        return []
    actions = []
    if not first:
        actions.append({
                "name": "offset",
                "text": "Previous",
                "type": "button",
                "value": __tmp6 - __tmp2
            })
    if not last:
        actions.append({
                "name": "offset",
                "text": "Next",
                "type": "button",
                "value": __tmp6 + __tmp2
            })
    return [{
        "text": "",
        "fallback": "",
        "callback_id": "leader_scroll",
        "attachment_type": "default",
        "actions": actions
    }]


# depreciated
def __tmp5(__tmp0: __typ0, ephemeral: bool = True) :
    logger.debug(f"Scoreboard request: {__tmp0}")
    team_id = __tmp0.get('team_id', '')
    with connect() as conn:
        __tmp3 = check_all_scores(conn, team_id)
    text = _parse_entire_scoreboard(__tmp3)
    return ephemeral_resp(text) if ephemeral else channel_resp(text)


# depreciated
def _parse_entire_scoreboard(__tmp3) -> str:
    text = f'Here\'s a list of my favourite people:'
    for index, (subject, score) in enumerate(__tmp3):
        text += f'\n{index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0:
            text += ' :crown:'
        elif index + 1 == len(__tmp3):
            text += ' :hankey:'
    return text
