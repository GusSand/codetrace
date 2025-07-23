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

def __tmp5(__tmp1: Mapping[str, Any],
                         __tmp7: Optional[str]) -> Optional[Tuple[str, str]]:
    __tmp7 = get_proper_action(__tmp1, __tmp7)
    if __tmp7 is not None:
        return __tmp3(__tmp1), __tmp2(__tmp1, __tmp7)
    return None

def get_proper_action(__tmp1: Mapping[str, Any], __tmp7: Optional[str]) -> Optional[str]:
    if __tmp7 == 'updateBoard':
        data = __tmp11(__tmp1)
        # we don't support events for when a board's background
        # is changed
        if data['old'].get('prefs', {}).get('background') is not None:
            return None
        elif data['old']['name']:
            return CHANGE_NAME
        raise UnknownUpdateBoardAction()
    return __tmp7

def __tmp3(__tmp1: Mapping[str, Any]) -> str:
    return __tmp11(__tmp1)['board']['name']

def __tmp2(__tmp1: Mapping[str, Any], __tmp7: <FILL>) -> str:
    message_body = ACTIONS_TO_FILL_BODY_MAPPER[__tmp7](__tmp1, __tmp7)
    creator = __tmp1['action']['memberCreator']['fullName']
    return u'{full_name} {rest}'.format(full_name=creator, rest=message_body)

def __tmp6(__tmp1: Mapping[str, Any], __tmp7: str) -> str:
    data = {
        'member_name': __tmp1['action']['member']['fullName'],
    }
    return __tmp10(__tmp1, __tmp7, data)

def get_create_list_body(__tmp1: Mapping[str, Any], __tmp7: str) -> str:
    data = {
        'list_name': __tmp11(__tmp1)['list']['name'],
    }
    return __tmp10(__tmp1, __tmp7, data)

def __tmp8(__tmp1: Mapping[str, Any], __tmp7: str) -> str:
    data = {
        'old_name': __tmp11(__tmp1)['old']['name']
    }
    return __tmp10(__tmp1, __tmp7, data)


def __tmp10(__tmp1: Mapping[str, Any],
                                     __tmp7,
                                     data: Optional[Dict[str, Any]]=None) -> str:
    data = {} if data is None else data
    data['board_url_template'] = data.get('board_url_template', __tmp4(__tmp1))
    message_body = get_message_body(__tmp7)
    return message_body.format(**data)

def __tmp4(__tmp1: Mapping[str, Any]) -> str:
    return TRELLO_BOARD_URL_TEMPLATE.format(board_name=__tmp0(__tmp1),
                                            board_url=__tmp9(__tmp1))

def __tmp0(__tmp1: Mapping[str, Any]) -> str:
    return __tmp11(__tmp1)['board']['name']

def __tmp9(__tmp1: Mapping[str, Any]) -> str:
    return u'https://trello.com/b/{}'.format(__tmp11(__tmp1)['board']['shortLink'])

def get_message_body(__tmp7: str) -> str:
    return ACTIONS_TO_MESSAGE_MAPPER[__tmp7]

def __tmp11(__tmp1: Mapping[str, Any]) -> Mapping[str, Any]:
    return __tmp1['action']['data']

ACTIONS_TO_FILL_BODY_MAPPER = {
    REMOVE_MEMBER: __tmp6,
    ADD_MEMBER: __tmp6,
    CREATE_LIST: get_create_list_body,
    CHANGE_NAME: __tmp8
}
