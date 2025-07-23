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


def __tmp5(__tmp0: __typ0, __tmp4: int = None, __tmp2: int = 10, ephemeral: __typ2 = True) -> Dict[__typ1, __typ1]:
    logger.debug(f"Scoreboard request: offset {__tmp4}; limit {__tmp2}; form: {__tmp0}")
    if 'command' in __tmp0:
        team_id = __tmp0['team_id']
        __tmp4 = __tmp4 if __tmp4 else 0
    else:
        team_id = __tmp0['team']['id']
        __tmp4 = __tmp4 if __tmp4 else int(__tmp0['actions'][0]['value'])

    with connect() as conn:
        # Try to fetch one more row. If limit + 1 rows come back, then there are more rows to display
        __tmp3 = check_scores(conn, team_id, __tmp4=__tmp4, __tmp2=__tmp2+1)
    text, __tmp7, last = _parse_scoreboard(__tmp3, __tmp4=__tmp4, __tmp2=__tmp2)

    attachments = __tmp6(__tmp7, last, __tmp4, __tmp2)
    return ephemeral_resp(text, attachments) if ephemeral else channel_resp(text, attachments)


def _parse_scoreboard(__tmp3: List[Tuple[__typ1, int]], __tmp4: <FILL>, __tmp2: int) -> Tuple[__typ1, __typ2, __typ2]:
    __tmp7 = (__tmp4 == 0)
    # last is an indicator to whether there are more results to display
    last = not (len(__tmp3) > __tmp2)
    if not last:
        # Then the last element of the scoreboard was just an indicator
        del(__tmp3[-1])

    text = f'Here\'s the points leaderboard:'
    for index, (subject, score) in enumerate(__tmp3):
        # offset+index+1 is the leaderboard position
        text += f'\n{__tmp4+index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0 and __tmp7:
            text += ' :crown:'
        elif index + 1 == len(__tmp3) and last:
            text += ' :hankey:'
    return text, __tmp7, last


def __tmp6(__tmp7: __typ2, last: __typ2, __tmp4, __tmp2: int):
    # Get the edge case out of the way:
    if __tmp7 and last:
        return []
    actions = []
    if not __tmp7:
        actions.append({
                "name": "offset",
                "text": "Previous",
                "type": "button",
                "value": __tmp4 - __tmp2
            })
    if not last:
        actions.append({
                "name": "offset",
                "text": "Next",
                "type": "button",
                "value": __tmp4 + __tmp2
            })
    return [{
        "text": "",
        "fallback": "",
        "callback_id": "leader_scroll",
        "attachment_type": "default",
        "actions": actions
    }]


# depreciated
def get_scoreboard(__tmp0: __typ0, ephemeral: __typ2 = True) -> Dict[__typ1, __typ1]:
    logger.debug(f"Scoreboard request: {__tmp0}")
    team_id = __tmp0.get('team_id', '')
    with connect() as conn:
        __tmp3 = check_all_scores(conn, team_id)
    text = __tmp1(__tmp3)
    return ephemeral_resp(text) if ephemeral else channel_resp(text)


# depreciated
def __tmp1(__tmp3: List[Tuple[__typ1, int]]) -> __typ1:
    text = f'Here\'s a list of my favourite people:'
    for index, (subject, score) in enumerate(__tmp3):
        text += f'\n{index+1}. <@{subject}> [{score} point{"s" if score != 1 else ""}]'
        if index == 0:
            text += ' :crown:'
        elif index + 1 == len(__tmp3):
            text += ' :hankey:'
    return text
