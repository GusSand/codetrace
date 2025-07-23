from typing import TypeAlias
__typ0 : TypeAlias = "Any"
__typ2 : TypeAlias = "int"
from zulip_bots.game_handler import GameAdapter, BadMoveException
from typing import List, Any


class GameHandlerBotMessageHandler(object):
    tokens = [':blue_circle:', ':red_circle:']

    def parse_board(__tmp0, __tmp1: __typ0) :
        return 'foo'

    def __tmp5(__tmp0, turn) :
        return __tmp0.tokens[turn]

    def alert_move_message(__tmp0, original_player: <FILL>, __tmp2: str) :
        column_number = __tmp2.replace('move ', '')
        return original_player + ' moved in column ' + column_number

    def game_start_message(__tmp0) :
        return 'Type `move <column>` to place a token.\n \
The first player to get 4 in a row wins!\n \
Good Luck!'


class __typ1(object):
    def __init__(__tmp0) :
        __tmp0.current_board = 'mock board'

    def make_move(
        __tmp0,
        __tmp3,
        player,
        is_computer: bool=False
    ) :
        if not is_computer:
            if __typ2(__tmp3.replace('move ', '')) < 9:
                return 'mock board'
            else:
                raise BadMoveException('Invalid Move.')
        return 'mock board'

    def __tmp4(__tmp0, players) :
        return None


class __typ3(GameAdapter):
    '''
    DO NOT USE THIS BOT
    This bot is used to test game_handler.py
    '''

    def __init__(__tmp0) -> None:
        game_name = 'foo test game'
        bot_name = 'game_handler_bot'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <column-number>```'
        move_regex = 'move (\d)$'
        model = __typ1
        gameMessageHandler = GameHandlerBotMessageHandler
        rules = ''

        super(__typ3, __tmp0).__init__(
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


handler_class = __typ3
