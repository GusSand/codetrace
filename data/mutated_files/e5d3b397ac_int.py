from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ5 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
import copy
import random

from typing import List, Any, Tuple, Dict
from zulip_bots.game_handler import GameAdapter, BadMoveException

class __typ3(object):

    final_board = [[0, 1, 2],
                   [3, 4, 5],
                   [6, 7, 8]]

    initial_board = [[8, 7, 6],
                     [5, 4, 3],
                     [2, 1, 0]]

    def __init__(__tmp2, board: __typ5=None) -> None:
        if board is not None:
            __tmp2.current_board = board
        else:
            __tmp2.current_board = copy.deepcopy(__tmp2.initial_board)

    def get_coordinates(__tmp2, board: List[List[int]]) :
        return {
            board[0][0]: (0, 0),
            board[0][1]: (0, 1),
            board[0][2]: (0, 2),
            board[1][0]: (1, 0),
            board[1][1]: (1, 1),
            board[1][2]: (1, 2),
            board[2][0]: (2, 0),
            board[2][1]: (2, 1),
            board[2][2]: (2, 2),
        }

    def determine_game_over(__tmp2, players) -> __typ1:
        if __tmp2.won(__tmp2.current_board):
            return 'current turn'
        return ''

    def won(__tmp2, board) :
        for i in range(3):
            for j in range(3):
                if (board[i][j] != __tmp2.final_board[i][j]):
                    return False
        return True

    def validate_move(__tmp2, tile: <FILL>) -> __typ4:
        if tile < 1 or tile > 8:
            return False
        return True

    def update_board(__tmp2, board):
        __tmp2.current_board = copy.deepcopy(board)

    def make_move(__tmp2, move: __typ1, __tmp1: int, computer_move: __typ4=False) :
        board = __tmp2.current_board
        move = move.strip()
        move = move.split(' ')

        if '' in move:
            raise BadMoveException('You should enter space separated digits.')
        moves = len(move)
        for m in range(1, moves):
            tile = int(move[m])
            coordinates = __tmp2.get_coordinates(board)
            if tile not in coordinates:
                raise BadMoveException('You can only move tiles which exist in the board.')
            i, j = coordinates[tile]
            if (j-1) > -1 and board[i][j-1] == 0:
                board[i][j-1] = tile
                board[i][j] = 0
            elif (i-1) > -1 and board[i-1][j] == 0:
                board[i-1][j] = tile
                board[i][j] = 0
            elif (j+1) < 3 and board[i][j+1] == 0:
                board[i][j+1] = tile
                board[i][j] = 0
            elif (i+1) < 3 and board[i+1][j] == 0:
                board[i+1][j] = tile
                board[i][j] = 0
            else:
                raise BadMoveException('You can only move tiles which are adjacent to :grey_question:.')
            if m == moves - 1:
                return board

class __typ2(object):

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

    def parse_board(__tmp2, board: __typ5) -> __typ1:
        # Header for the top of the board
        board_str = ''

        for row in range(3):
            board_str += '\n\n'
            for column in range(3):
                board_str += __tmp2.tiles[__typ1(board[row][column])]
        return board_str

    def __tmp0(__tmp2, original_player: __typ1, move_info: __typ1) -> __typ1:
        tile = move_info.replace('move ', '')
        return original_player + ' moved ' + tile

    def game_start_message(__tmp2) -> __typ1:
        return ("Welcome to Game of Fifteen!"
                "To make a move, type @-mention `move <tile1> <tile2> ...`")

class __typ0(GameAdapter):
    '''
    Bot that uses the Game Adapter class
    to allow users to play Game of Fifteen
    '''

    def __init__(__tmp2) -> None:
        game_name = 'Game of Fifteen'
        bot_name = 'Game of Fifteen'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <tile1> <tile2> ...```'
        move_regex = 'move [\d{1}\s]+$'
        model = __typ3
        gameMessageHandler = __typ2
        rules = '''Arrange the board’s tiles from smallest to largest, left to right,
                  top to bottom, and tiles adjacent to :grey_question: can only be moved.
                  Final configuration will have :grey_question: in top left.'''

        super(__typ0, __tmp2).__init__(
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

handler_class = __typ0
