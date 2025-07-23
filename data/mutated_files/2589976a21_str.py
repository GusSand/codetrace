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
                         __tmp3) :
    __tmp3 = get_proper_action(__tmp1, __tmp3)
    if __tmp3 is not None:
        return get_subject(__tmp1), get_body(__tmp1, __tmp3)
    return None

def get_proper_action(__tmp1, __tmp3) :
    if __tmp3 == 'updateBoard':
        data = __tmp4(__tmp1)
        # we don't support events for when a board's background
        # is changed
        if data['old'].get('prefs', {}).get('background') is not None:
            return None
        elif data['old']['name']:
            return CHANGE_NAME
        raise UnknownUpdateBoardAction()
    return __tmp3

def get_subject(__tmp1: Mapping[str, Any]) -> str:
    return __tmp4(__tmp1)['board']['name']

def get_body(__tmp1: Mapping[str, Any], __tmp3) -> str:
    message_body = ACTIONS_TO_FILL_BODY_MAPPER[__tmp3](__tmp1, __tmp3)
    creator = __tmp1['action']['memberCreator']['fullName']
    return u'{full_name} {rest}'.format(full_name=creator, rest=message_body)

def get_managed_member_body(__tmp1: Mapping[str, Any], __tmp3) -> str:
    data = {
        'member_name': __tmp1['action']['member']['fullName'],
    }
    return fill_appropriate_message_content(__tmp1, __tmp3, data)

def get_create_list_body(__tmp1: Mapping[str, Any], __tmp3: str) -> str:
    data = {
        'list_name': __tmp4(__tmp1)['list']['name'],
    }
    return fill_appropriate_message_content(__tmp1, __tmp3, data)

def get_change_name_body(__tmp1: Mapping[str, Any], __tmp3: <FILL>) :
    data = {
        'old_name': __tmp4(__tmp1)['old']['name']
    }
    return fill_appropriate_message_content(__tmp1, __tmp3, data)


def fill_appropriate_message_content(__tmp1: Mapping[str, Any],
                                     __tmp3,
                                     data: Optional[Dict[str, Any]]=None) :
    data = {} if data is None else data
    data['board_url_template'] = data.get('board_url_template', __tmp2(__tmp1))
    message_body = get_message_body(__tmp3)
    return message_body.format(**data)

def __tmp2(__tmp1) :
    return TRELLO_BOARD_URL_TEMPLATE.format(board_name=__tmp0(__tmp1),
                                            board_url=get_board_url(__tmp1))

def __tmp0(__tmp1) :
    return __tmp4(__tmp1)['board']['name']

def get_board_url(__tmp1) -> str:
    return u'https://trello.com/b/{}'.format(__tmp4(__tmp1)['board']['shortLink'])

def get_message_body(__tmp3) -> str:
    return ACTIONS_TO_MESSAGE_MAPPER[__tmp3]

def __tmp4(__tmp1) :
    return __tmp1['action']['data']

ACTIONS_TO_FILL_BODY_MAPPER = {
    REMOVE_MEMBER: get_managed_member_body,
    ADD_MEMBER: get_managed_member_body,
    CREATE_LIST: get_create_list_body,
    CHANGE_NAME: get_change_name_body
}
