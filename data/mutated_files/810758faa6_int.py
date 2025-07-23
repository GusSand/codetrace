from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "ImmutableMultiDict"
__typ1 : TypeAlias = "str"
import logging
from typing import Dict, List, Tuple

from werkzeug.datastructures import ImmutableMultiDict

from pointy.database.common import connect, channel_resp, ephemeral_resp
from pointy.database.team import check_scores, check_all_scores

logger = logging.getLogger(__name__)


def __tmp7(__tmp0, __tmp10: int = None, __tmp4: int = 10, ephemeral: __typ2 = True) :
    logger.debug(f"Scoreboard request: offset {__tmp10}; limit {__tmp4}; form: {__tmp0}")
    if 'command' in __tmp0:
        team_id = __tmp0['team_id']
        __tmp10 = __tmp10 if __tmp10 else 0
    else:
        team_id = __tmp0['team']['id']
        __tmp10 = __tmp10 if __tmp10 else int(__tmp0['actions'][0]['value'])

    with connect() as conn:
        # Try to fetch one more row. If limit + 1 rows come back, then there are more rows to display
        __tmp5 = check_scores(conn, team_id, __tmp10=__tmp10, __tmp4=__tmp4+1)
    text, __tmp6, __tmp1 = __tmp3(__tmp5, __tmp10=__tmp10, __tmp4=__tmp4)

    attachments = __tmp9(__tmp6, __tmp1, __tmp10, __tmp4)
    return ephemeral_resp(text, attachments) if ephemeral else channel_resp(text, attachments)


def __tmp3(__tmp5, __tmp10, __tmp4) :
    __tmp6 = (__tmp10 == 0)
    # last is an indicator to whether there are more results to display
    __tmp1 = not (len(__tmp5) > __tmp4)
    if not __tmp1:
        # Then the last element of the scoreboard was just an indicator
        del(__tmp5[-1])

    text = f'Here\'s the points leaderboard:'
    for index, (subject, score) in enumerate(__tmp5):
        # offset+index+1 is the leaderboard position
        text += f'\n{__tmp10+index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0 and __tmp6:
            text += ' :crown:'
        elif index + 1 == len(__tmp5) and __tmp1:
            text += ' :hankey:'
    return text, __tmp6, __tmp1


def __tmp9(__tmp6, __tmp1, __tmp10: <FILL>, __tmp4: int):
    # Get the edge case out of the way:
    if __tmp6 and __tmp1:
        return []
    actions = []
    if not __tmp6:
        actions.append({
                "name": "offset",
                "text": "Previous",
                "type": "button",
                "value": __tmp10 - __tmp4
            })
    if not __tmp1:
        actions.append({
                "name": "offset",
                "text": "Next",
                "type": "button",
                "value": __tmp10 + __tmp4
            })
    return [{
        "text": "",
        "fallback": "",
        "callback_id": "leader_scroll",
        "attachment_type": "default",
        "actions": actions
    }]


# depreciated
def __tmp8(__tmp0, ephemeral: __typ2 = True) :
    logger.debug(f"Scoreboard request: {__tmp0}")
    team_id = __tmp0.get('team_id', '')
    with connect() as conn:
        __tmp5 = check_all_scores(conn, team_id)
    text = __tmp2(__tmp5)
    return ephemeral_resp(text) if ephemeral else channel_resp(text)


# depreciated
def __tmp2(__tmp5) :
    text = f'Here\'s a list of my favourite people:'
    for index, (subject, score) in enumerate(__tmp5):
        text += f'\n{index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0:
            text += ' :crown:'
        elif index + 1 == len(__tmp5):
            text += ' :hankey:'
    return text
