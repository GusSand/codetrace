from zulip_bots.game_handler import GameAdapter
from zulip_bots.bots.connect_four.controller import ConnectFourModel
from typing import Any


class ConnectFourMessageHandler(object):
    tokens = [':blue_circle:', ':red_circle:']

    def parse_board(__tmp0, board: <FILL>) :
        # Header for the top of the board
        board_str = ':one: :two: :three: :four: :five: :six: :seven:'

        for row in range(0, 6):
            board_str += '\n\n'
            for column in range(0, 7):
                if board[row][column] == 0:
                    board_str += ':heavy_large_circle: '
                elif board[row][column] == 1:
                    board_str += ':blue_circle: '
                elif board[row][column] == -1:
                    board_str += ':red_circle: '

        return board_str

    def __tmp3(__tmp0, turn: int) -> str:
        return __tmp0.tokens[turn]

    def __tmp2(__tmp0, __tmp4: str, __tmp1: str) -> str:
        column_number = __tmp1.replace('move ', '')
        return __tmp4 + ' moved in column ' + column_number

    def game_start_message(__tmp0) :
        return 'Type `move <column-number>` or `<column-number>` to place a token.\n\
The first player to get 4 in a row wins!\n Good Luck!'


class __typ0(GameAdapter):
    '''
    Bot that uses the Game Adapter class
    to allow users to play other users
    or the comptuer in a game of Connect
    Four
    '''

    def __init__(__tmp0) -> None:
        game_name = 'Connect Four'
        bot_name = 'connect_four'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <column-number>``` or ```<column-number>```'
        move_regex = '(move ([1-7])$)|(([1-7])$)'
        model = ConnectFourModel
        gameMessageHandler = ConnectFourMessageHandler
        rules = '''Try to get four pieces in row, Diagonals count too!'''

        super(__typ0, __tmp0).__init__(
            game_name,
            bot_name,
            move_help_message,
            move_regex,
            model,
            gameMessageHandler,
            rules,
            max_players=2
        )


handler_class = __typ0
