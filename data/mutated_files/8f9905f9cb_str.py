from typing import TypeAlias
__typ0 : TypeAlias = "Any"
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

    def __init__(__tmp1, __tmp8):
        __tmp1.data[__tmp8] = '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'

    def put(__tmp1, __tmp8, value):
        __tmp1.data[__tmp8] = value

    def get(__tmp1, __tmp8):
        return __tmp1.data[__tmp8]

class MerelsModel(object):

    def __init__(__tmp1, __tmp2: __typ0=None) :
        __tmp1.topic = "merels"
        __tmp1.storage = Storage(__tmp1.topic)
        __tmp1.current_board = mechanics.display_game(__tmp1.topic, __tmp1.storage)
        __tmp1.token = ['O', 'X']

    def __tmp10(__tmp1, __tmp9) :
        if __tmp1.contains_winning_move(__tmp1.current_board):
            return 'current turn'
        return ''

    def contains_winning_move(__tmp1, __tmp2) :
        merels = database.MerelsStorage(__tmp1.topic, __tmp1.storage)
        data = game_data.GameData(merels.get_game_data(__tmp1.topic))

        if data.get_phase() > 1:
            if (mechanics.get_piece("X", data.grid()) <= 2) or\
                    (mechanics.get_piece("O", data.grid()) <= 2):
                return True
        return False

    def make_move(__tmp1, __tmp7: <FILL>, __tmp0, computer_move: bool=False) :
        if __tmp1.storage.get(__tmp1.topic) == '["X", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]':
            __tmp1.storage.put(
                __tmp1.topic,
                '["{}", 0, 0, "NNNNNNNNNNNNNNNNNNNNNNNN", "", 0]'.format(
                    __tmp1.token[__tmp0]
                ))
        __tmp1.current_board, same_player_move = game.beat(__tmp7, __tmp1.topic, __tmp1.storage)
        if same_player_move != "":
            raise SamePlayerMove(same_player_move)
        return __tmp1.current_board

class MerelsMessageHandler(object):
    tokens = [':o_button:', ':cross_mark_button:']

    def __tmp11(__tmp1, __tmp2) -> str:
        return __tmp2

    def __tmp12(__tmp1, __tmp3) :
        return __tmp1.tokens[__tmp3]

    def __tmp6(__tmp1, __tmp14, __tmp4) :
        return __tmp14 + " :" + __tmp4

    def __tmp5(__tmp1) :
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

    def __tmp13(__tmp1) :
        return game.getInfo()

    def __init__(__tmp1) :
        game_name = 'Merels'
        bot_name = 'merels'
        move_help_message = ""
        move_regex = '.*'
        model = MerelsModel
        rules = game.getInfo()
        gameMessageHandler = MerelsMessageHandler
        super(MerelsHandler, __tmp1).__init__(
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
