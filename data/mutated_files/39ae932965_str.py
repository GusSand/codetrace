from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
import copy
import random

from typing import List, Any, Tuple, Dict
from zulip_bots.game_handler import GameAdapter, BadMoveException

class GameOfFifteenModel(object):

    final_board = [[0, 1, 2],
                   [3, 4, 5],
                   [6, 7, 8]]

    initial_board = [[8, 7, 6],
                     [5, 4, 3],
                     [2, 1, 0]]

    def __init__(__tmp1, __tmp2: __typ3=None) -> None:
        if __tmp2 is not None:
            __tmp1.current_board = __tmp2
        else:
            __tmp1.current_board = copy.deepcopy(__tmp1.initial_board)

    def get_coordinates(__tmp1, __tmp2) -> Dict[__typ0, Tuple[__typ0, __typ0]]:
        return {
            __tmp2[0][0]: (0, 0),
            __tmp2[0][1]: (0, 1),
            __tmp2[0][2]: (0, 2),
            __tmp2[1][0]: (1, 0),
            __tmp2[1][1]: (1, 1),
            __tmp2[1][2]: (1, 2),
            __tmp2[2][0]: (2, 0),
            __tmp2[2][1]: (2, 1),
            __tmp2[2][2]: (2, 2),
        }

    def __tmp7(__tmp1, __tmp6: List[str]) :
        if __tmp1.won(__tmp1.current_board):
            return 'current turn'
        return ''

    def won(__tmp1, __tmp2) -> __typ2:
        for i in range(3):
            for j in range(3):
                if (__tmp2[i][j] != __tmp1.final_board[i][j]):
                    return False
        return True

    def validate_move(__tmp1, __tmp8: __typ0) :
        if __tmp8 < 1 or __tmp8 > 8:
            return False
        return True

    def update_board(__tmp1, __tmp2):
        __tmp1.current_board = copy.deepcopy(__tmp2)

    def make_move(__tmp1, __tmp5, __tmp0, computer_move: __typ2=False) -> __typ3:
        __tmp2 = __tmp1.current_board
        __tmp5 = __tmp5.strip()
        __tmp5 = __tmp5.split(' ')

        if '' in __tmp5:
            raise BadMoveException('You should enter space separated digits.')
        moves = len(__tmp5)
        for m in range(1, moves):
            __tmp8 = __typ0(__tmp5[m])
            coordinates = __tmp1.get_coordinates(__tmp2)
            if __tmp8 not in coordinates:
                raise BadMoveException('You can only move tiles which exist in the board.')
            i, j = coordinates[__tmp8]
            if (j-1) > -1 and __tmp2[i][j-1] == 0:
                __tmp2[i][j-1] = __tmp8
                __tmp2[i][j] = 0
            elif (i-1) > -1 and __tmp2[i-1][j] == 0:
                __tmp2[i-1][j] = __tmp8
                __tmp2[i][j] = 0
            elif (j+1) < 3 and __tmp2[i][j+1] == 0:
                __tmp2[i][j+1] = __tmp8
                __tmp2[i][j] = 0
            elif (i+1) < 3 and __tmp2[i+1][j] == 0:
                __tmp2[i+1][j] = __tmp8
                __tmp2[i][j] = 0
            else:
                raise BadMoveException('You can only move tiles which are adjacent to :grey_question:.')
            if m == moves - 1:
                return __tmp2

class __typ1(object):

    tiles = {
        '0': ':grey_question:',
        '1': ':one:',
        '2': ':two:',
        '3': ':three:',
        '4': ':four:',
        '5': ':five:',
        '6': ':six:',
        '7': ':seven:',
        '8': ':eight:',
    }

    def parse_board(__tmp1, __tmp2) -> str:
        # Header for the top of the board
        board_str = ''

        for row in range(3):
            board_str += '\n\n'
            for column in range(3):
                board_str += __tmp1.tiles[str(__tmp2[row][column])]
        return board_str

    def alert_move_message(__tmp1, __tmp9, __tmp3: <FILL>) :
        __tmp8 = __tmp3.replace('move ', '')
        return __tmp9 + ' moved ' + __tmp8

    def __tmp4(__tmp1) :
        return ("Welcome to Game of Fifteen!"
                "To make a move, type @-mention `move <tile1> <tile2> ...`")

class GameOfFifteenBotHandler(GameAdapter):
    '''
    Bot that uses the Game Adapter class
    to allow users to play Game of Fifteen
    '''

    def __init__(__tmp1) -> None:
        game_name = 'Game of Fifteen'
        bot_name = 'Game of Fifteen'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <tile1> <tile2> ...```'
        move_regex = 'move [\d{1}\s]+$'
        model = GameOfFifteenModel
        gameMessageHandler = __typ1
        rules = '''Arrange the board’s tiles from smallest to largest, left to right,
                  top to bottom, and tiles adjacent to :grey_question: can only be moved.
                  Final configuration will have :grey_question: in top left.'''

        super(GameOfFifteenBotHandler, __tmp1).__init__(
            game_name,
            bot_name,
            move_help_message,
            move_regex,
            model,
            gameMessageHandler,
            rules,
            min_players=1,
            max_players=1,
        )

handler_class = GameOfFifteenBotHandler
