from typing import Any, Dict, Mapping, MutableMapping, Optional, Tuple

from .exceptions import UnknownUpdateBoardAction

SUPPORTED_BOARD_ACTIONS = [
    u'removeMemberFromBoard',
    u'addMemberToBoard',
    u'createList',
    u'updateBoard',
]

REMOVE_MEMBER = u'removeMemberFromBoard'
ADD_MEMBER = u'addMemberToBoard'
CREATE_LIST = u'createList'
CHANGE_NAME = u'changeName'

TRELLO_BOARD_URL_TEMPLATE = u'[{board_name}]({board_url})'

ACTIONS_TO_MESSAGE_MAPPER = {
    REMOVE_MEMBER: u'removed {member_name} from {board_url_template}.',
    ADD_MEMBER: u'added {member_name} to {board_url_template}.',
    CREATE_LIST: u'added {list_name} list to {board_url_template}.',
    CHANGE_NAME: u'renamed the board from {old_name} to {board_url_template}.'
}

def process_board_action(__tmp1: Mapping[str, Any],
                         __tmp4) -> Optional[Tuple[str, str]]:
    __tmp4 = __tmp3(__tmp1, __tmp4)
    if __tmp4 is not None:
        return __tmp2(__tmp1), get_body(__tmp1, __tmp4)
    return None

def __tmp3(__tmp1, __tmp4) -> Optional[str]:
    if __tmp4 == 'updateBoard':
        data = get_action_data(__tmp1)
        # we don't support events for when a board's background
        # is changed
        if data['old'].get('prefs', {}).get('background') is not None:
            return None
        elif data['old']['name']:
            return CHANGE_NAME
        raise UnknownUpdateBoardAction()
    return __tmp4

def __tmp2(__tmp1: Mapping[str, Any]) :
    return get_action_data(__tmp1)['board']['name']

def get_body(__tmp1: Mapping[str, Any], __tmp4: str) -> str:
    message_body = ACTIONS_TO_FILL_BODY_MAPPER[__tmp4](__tmp1, __tmp4)
    creator = __tmp1['action']['memberCreator']['fullName']
    return u'{full_name} {rest}'.format(full_name=creator, rest=message_body)

def get_managed_member_body(__tmp1, __tmp4) :
    data = {
        'member_name': __tmp1['action']['member']['fullName'],
    }
    return fill_appropriate_message_content(__tmp1, __tmp4, data)

def get_create_list_body(__tmp1, __tmp4: <FILL>) :
    data = {
        'list_name': get_action_data(__tmp1)['list']['name'],
    }
    return fill_appropriate_message_content(__tmp1, __tmp4, data)

def __tmp5(__tmp1: Mapping[str, Any], __tmp4: str) :
    data = {
        'old_name': get_action_data(__tmp1)['old']['name']
    }
    return fill_appropriate_message_content(__tmp1, __tmp4, data)


def fill_appropriate_message_content(__tmp1,
                                     __tmp4,
                                     data: Optional[Dict[str, Any]]=None) -> str:
    data = {} if data is None else data
    data['board_url_template'] = data.get('board_url_template', get_filled_board_url_template(__tmp1))
    message_body = get_message_body(__tmp4)
    return message_body.format(**data)

def get_filled_board_url_template(__tmp1: Mapping[str, Any]) :
    return TRELLO_BOARD_URL_TEMPLATE.format(board_name=__tmp0(__tmp1),
                                            board_url=get_board_url(__tmp1))

def __tmp0(__tmp1: Mapping[str, Any]) :
    return get_action_data(__tmp1)['board']['name']

def get_board_url(__tmp1: Mapping[str, Any]) :
    return u'https://trello.com/b/{}'.format(get_action_data(__tmp1)['board']['shortLink'])

def get_message_body(__tmp4: str) -> str:
    return ACTIONS_TO_MESSAGE_MAPPER[__tmp4]

def get_action_data(__tmp1) :
    return __tmp1['action']['data']

ACTIONS_TO_FILL_BODY_MAPPER = {
    REMOVE_MEMBER: get_managed_member_body,
    ADD_MEMBER: get_managed_member_body,
    CREATE_LIST: get_create_list_body,
    CHANGE_NAME: __tmp5
}
