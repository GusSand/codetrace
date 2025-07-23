from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
from zulip_bots.game_handler import GameAdapter, BadMoveException
from typing import List, Any


class GameHandlerBotMessageHandler(object):
    tokens = [':blue_circle:', ':red_circle:']

    def __tmp0(__tmp2, board: __typ2) :
        return 'foo'

    def get_player_color(__tmp2, turn) :
        return __tmp2.tokens[turn]

    def __tmp1(__tmp2, original_player, move_info: str) -> str:
        column_number = move_info.replace('move ', '')
        return original_player + ' moved in column ' + column_number

    def game_start_message(__tmp2) -> str:
        return 'Type `move <column>` to place a token.\n \
The first player to get 4 in a row wins!\n \
Good Luck!'


class MockModel(object):
    def __init__(__tmp2) -> None:
        __tmp2.current_board = 'mock board'

    def __tmp3(
        __tmp2,
        move: <FILL>,
        player: __typ0,
        is_computer: bool=False
    ) :
        if not is_computer:
            if __typ0(move.replace('move ', '')) < 9:
                return 'mock board'
            else:
                raise BadMoveException('Invalid Move.')
        return 'mock board'

    def determine_game_over(__tmp2, players: List[str]) :
        return None


class __typ1(GameAdapter):
    '''
    DO NOT USE THIS BOT
    This bot is used to test game_handler.py
    '''

    def __init__(__tmp2) -> None:
        game_name = 'foo test game'
        bot_name = 'game_handler_bot'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <column-number>```'
        move_regex = 'move (\d)$'
        model = MockModel
        gameMessageHandler = GameHandlerBotMessageHandler
        rules = ''

        super(__typ1, __tmp2).__init__(
            game_name,
            bot_name,
            move_help_message,
            move_regex,
            model,
            gameMessageHandler,
            rules,
            max_players=2,
            supports_computer=True
        )


handler_class = __typ1
