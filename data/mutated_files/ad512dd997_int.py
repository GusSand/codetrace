from typing import TypeAlias
__typ3 : TypeAlias = "Any"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
from typing import List, Any
from zulip_bots.bots.merels.libraries import (
    game,
    mechanics,
    database,
    game_data
)
from zulip_bots.game_handler import GameAdapter, SamePlayerMove, GameInstance

class __typ4(object):
    data = {}

    def __init__(__tmp1, __tmp4):
        __tmp1.data[__tmp4] = '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'

    def put(__tmp1, __tmp4, value: __typ0):
        __tmp1.data[__tmp4] = value

    def get(__tmp1, __tmp4):
        return __tmp1.data[__tmp4]

class MerelsModel(object):

    def __init__(__tmp1, __tmp2: __typ3=None) -> None:
        __tmp1.topic = "merels"
        __tmp1.storage = __typ4(__tmp1.topic)
        __tmp1.current_board = mechanics.display_game(__tmp1.topic, __tmp1.storage)
        __tmp1.token = ['O', 'X']

    def determine_game_over(__tmp1, players: List[__typ0]) :
        if __tmp1.contains_winning_move(__tmp1.current_board):
            return 'current turn'
        return ''

    def contains_winning_move(__tmp1, __tmp2: __typ3) ->__typ2:
        merels = database.MerelsStorage(__tmp1.topic, __tmp1.storage)
        data = game_data.GameData(merels.get_game_data(__tmp1.topic))

        if data.get_phase() > 1:
            if (mechanics.get_piece("X", data.grid()) <= 2) or\
                    (mechanics.get_piece("O", data.grid()) <= 2):
                return True
        return False

    def __tmp3(__tmp1, __tmp6: __typ0, __tmp0: int, computer_move: __typ2=False) -> __typ3:
        if __tmp1.storage.get(__tmp1.topic) == '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]':
            __tmp1.storage.put(
                __tmp1.topic,
                '["{}", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'.format(
                    __tmp1.token[__tmp0]
                ))
        __tmp1.current_board, same_player_move = game.beat(__tmp6, __tmp1.topic, __tmp1.storage)
        if same_player_move != "":
            raise SamePlayerMove(same_player_move)
        return __tmp1.current_board

class MerelsMessageHandler(object):
    tokens = [':o_button:', ':cross_mark_button:']

    def parse_board(__tmp1, __tmp2: __typ3) -> __typ0:
        return __tmp2

    def __tmp8(__tmp1, turn: <FILL>) -> __typ0:
        return __tmp1.tokens[turn]

    def __tmp7(__tmp1, original_player: __typ0, move_info: __typ0) -> __typ0:
        return original_player + " :" + move_info

    def __tmp5(__tmp1) -> __typ0:
        return game.getHelp()

class __typ1(GameAdapter):
    '''
    You can play merels! Make sure your message starts with
    "@mention-bot".
    '''
    META = {
        'name': 'merels',
        'description': 'Lets you play merels against any player.',
    }

    def usage(__tmp1) -> __typ0:
        return game.getInfo()

    def __init__(__tmp1) -> None:
        game_name = 'Merels'
        bot_name = 'merels'
        move_help_message = ""
        move_regex = '.*'
        model = MerelsModel
        rules = game.getInfo()
        gameMessageHandler = MerelsMessageHandler
        super(__typ1, __tmp1).__init__(
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

handler_class = __typ1
