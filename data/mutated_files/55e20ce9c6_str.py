from typing import TypeAlias
__typ0 : TypeAlias = "int"
from zulip_bots.game_handler import GameAdapter
from zulip_bots.bots.connect_four.controller import ConnectFourModel
from typing import Any


class __typ1(object):
    tokens = [':blue_circle:', ':red_circle:']

    def __tmp1(__tmp2, __tmp3: Any) :
        # Header for the top of the board
        board_str = ':one: :two: :three: :four: :five: :six: :seven:'

        for row in range(0, 6):
            board_str += '\n\n'
            for column in range(0, 7):
                if __tmp3[row][column] == 0:
                    board_str += ':heavy_large_circle: '
                elif __tmp3[row][column] == 1:
                    board_str += ':blue_circle: '
                elif __tmp3[row][column] == -1:
                    board_str += ':red_circle: '

        return board_str

    def get_player_color(__tmp2, turn: __typ0) -> str:
        return __tmp2.tokens[turn]

    def alert_move_message(__tmp2, original_player: str, __tmp0: <FILL>) -> str:
        column_number = __tmp0.replace('move ', '')
        return original_player + ' moved in column ' + column_number

    def game_start_message(__tmp2) :
        return 'Type `move <column-number>` or `<column-number>` to place a token.\n\
The first player to get 4 in a row wins!\n Good Luck!'


class __typ2(GameAdapter):
    '''
    Bot that uses the Game Adapter class
    to allow users to play other users
    or the comptuer in a game of Connect
    Four
    '''

    def __init__(__tmp2) :
        game_name = 'Connect Four'
        bot_name = 'connect_four'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <column-number>``` or ```<column-number>```'
        move_regex = '(move ([1-7])$)|(([1-7])$)'
        model = ConnectFourModel
        gameMessageHandler = __typ1
        rules = '''Try to get four pieces in row, Diagonals count too!'''

        super(__typ2, __tmp2).__init__(
            game_name,
            bot_name,
            move_help_message,
            move_regex,
            model,
            gameMessageHandler,
            rules,
            max_players=2
        )


handler_class = __typ2
