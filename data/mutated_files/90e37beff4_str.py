from typing import TypeAlias
__typ4 : TypeAlias = "Any"
__typ3 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
from typing import List, Any
from zulip_bots.bots.merels.libraries import (
    game,
    mechanics,
    database,
    game_data
)
from zulip_bots.game_handler import GameAdapter, SamePlayerMove, GameInstance

class __typ5(object):
    data = {}

    def __init__(__tmp0, __tmp6):
        __tmp0.data[__tmp6] = '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'

    def put(__tmp0, __tmp6, __tmp3: <FILL>):
        __tmp0.data[__tmp6] = __tmp3

    def get(__tmp0, __tmp6):
        return __tmp0.data[__tmp6]

class __typ6(object):

    def __init__(__tmp0, __tmp1: __typ4=None) -> None:
        __tmp0.topic = "merels"
        __tmp0.storage = __typ5(__tmp0.topic)
        __tmp0.current_board = mechanics.display_game(__tmp0.topic, __tmp0.storage)
        __tmp0.token = ['O', 'X']

    def __tmp11(__tmp0, __tmp9) :
        if __tmp0.contains_winning_move(__tmp0.current_board):
            return 'current turn'
        return ''

    def contains_winning_move(__tmp0, __tmp1) :
        merels = database.MerelsStorage(__tmp0.topic, __tmp0.storage)
        data = game_data.GameData(merels.get_game_data(__tmp0.topic))

        if data.get_phase() > 1:
            if (mechanics.get_piece("X", data.grid()) <= 2) or\
                    (mechanics.get_piece("O", data.grid()) <= 2):
                return True
        return False

    def __tmp5(__tmp0, __tmp8, player_number, computer_move: __typ3=False) -> __typ4:
        if __tmp0.storage.get(__tmp0.topic) == '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]':
            __tmp0.storage.put(
                __tmp0.topic,
                '["{}", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'.format(
                    __tmp0.token[player_number]
                ))
        __tmp0.current_board, same_player_move = game.beat(__tmp8, __tmp0.topic, __tmp0.storage)
        if same_player_move != "":
            raise SamePlayerMove(same_player_move)
        return __tmp0.current_board

class __typ1(object):
    tokens = [':o_button:', ':cross_mark_button:']

    def __tmp12(__tmp0, __tmp1) :
        return __tmp1

    def get_player_color(__tmp0, __tmp2) :
        return __tmp0.tokens[__tmp2]

    def __tmp10(__tmp0, __tmp14, __tmp4) -> str:
        return __tmp14 + " :" + __tmp4

    def __tmp7(__tmp0) :
        return game.getHelp()

class __typ2(GameAdapter):
    '''
    You can play merels! Make sure your message starts with
    "@mention-bot".
    '''
    META = {
        'name': 'merels',
        'description': 'Lets you play merels against any player.',
    }

    def __tmp13(__tmp0) -> str:
        return game.getInfo()

    def __init__(__tmp0) -> None:
        game_name = 'Merels'
        bot_name = 'merels'
        move_help_message = ""
        move_regex = '.*'
        model = __typ6
        rules = game.getInfo()
        gameMessageHandler = __typ1
        super(__typ2, __tmp0).__init__(
            game_name,
            bot_name,
            move_help_message,
            move_regex,
            model,
            gameMessageHandler,
            rules,
            max_players = 2,
            min_players = 2,
            supports_computer=False
        )

handler_class = __typ2
