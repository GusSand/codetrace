from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
from typing import List, Any
from zulip_bots.bots.merels.libraries import (
    game,
    mechanics,
    database,
    game_data
)
from zulip_bots.game_handler import GameAdapter, SamePlayerMove, GameInstance

class Storage(object):
    data = {}

    def __init__(__tmp0, __tmp2):
        __tmp0.data[__tmp2] = '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'

    def put(__tmp0, __tmp2, value):
        __tmp0.data[__tmp2] = value

    def get(__tmp0, __tmp2):
        return __tmp0.data[__tmp2]

class MerelsModel(object):

    def __init__(__tmp0, board: __typ2=None) :
        __tmp0.topic = "merels"
        __tmp0.storage = Storage(__tmp0.topic)
        __tmp0.current_board = mechanics.display_game(__tmp0.topic, __tmp0.storage)
        __tmp0.token = ['O', 'X']

    def determine_game_over(__tmp0, __tmp3: List[__typ0]) :
        if __tmp0.contains_winning_move(__tmp0.current_board):
            return 'current turn'
        return ''

    def contains_winning_move(__tmp0, board) :
        merels = database.MerelsStorage(__tmp0.topic, __tmp0.storage)
        data = game_data.GameData(merels.get_game_data(__tmp0.topic))

        if data.get_phase() > 1:
            if (mechanics.get_piece("X", data.grid()) <= 2) or\
                    (mechanics.get_piece("O", data.grid()) <= 2):
                return True
        return False

    def __tmp1(__tmp0, move, player_number: <FILL>, computer_move: __typ1=False) :
        if __tmp0.storage.get(__tmp0.topic) == '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]':
            __tmp0.storage.put(
                __tmp0.topic,
                '["{}", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'.format(
                    __tmp0.token[player_number]
                ))
        __tmp0.current_board, same_player_move = game.beat(move, __tmp0.topic, __tmp0.storage)
        if same_player_move != "":
            raise SamePlayerMove(same_player_move)
        return __tmp0.current_board

class MerelsMessageHandler(object):
    tokens = [':o_button:', ':cross_mark_button:']

    def __tmp4(__tmp0, board) :
        return board

    def get_player_color(__tmp0, turn) -> __typ0:
        return __tmp0.tokens[turn]

    def alert_move_message(__tmp0, original_player, move_info) :
        return original_player + " :" + move_info

    def game_start_message(__tmp0) :
        return game.getHelp()

class MerelsHandler(GameAdapter):
    '''
    You can play merels! Make sure your message starts with
    "@mention-bot".
    '''
    META = {
        'name': 'merels',
        'description': 'Lets you play merels against any player.',
    }

    def usage(__tmp0) :
        return game.getInfo()

    def __init__(__tmp0) :
        game_name = 'Merels'
        bot_name = 'merels'
        move_help_message = ""
        move_regex = '.*'
        model = MerelsModel
        rules = game.getInfo()
        gameMessageHandler = MerelsMessageHandler
        super(MerelsHandler, __tmp0).__init__(
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

handler_class = MerelsHandler
