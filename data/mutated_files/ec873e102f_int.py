from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
from zulip_bots.game_handler import GameAdapter, BadMoveException
from typing import List, Any


class __typ0(object):
    tokens = [':blue_circle:', ':red_circle:']

    def __tmp6(__tmp0, __tmp1) :
        return 'foo'

    def get_player_color(__tmp0, __tmp2: int) :
        return __tmp0.tokens[__tmp2]

    def alert_move_message(__tmp0, __tmp7, __tmp3: __typ1) :
        column_number = __tmp3.replace('move ', '')
        return __tmp7 + ' moved in column ' + column_number

    def game_start_message(__tmp0) :
        return 'Type `move <column>` to place a token.\n \
The first player to get 4 in a row wins!\n \
Good Luck!'


class MockModel(object):
    def __init__(__tmp0) :
        __tmp0.current_board = 'mock board'

    def __tmp4(
        __tmp0,
        __tmp5,
        player: <FILL>,
        is_computer: bool=False
    ) -> __typ2:
        if not is_computer:
            if int(__tmp5.replace('move ', '')) < 9:
                return 'mock board'
            else:
                raise BadMoveException('Invalid Move.')
        return 'mock board'

    def determine_game_over(__tmp0, players) -> None:
        return None


class GameHandlerBotHandler(GameAdapter):
    '''
    DO NOT USE THIS BOT
    This bot is used to test game_handler.py
    '''

    def __init__(__tmp0) :
        game_name = 'foo test game'
        bot_name = 'game_handler_bot'
        move_help_message = '* To make your move during a game, type\n' \
                            '```move <column-number>```'
        move_regex = 'move (\d)$'
        model = MockModel
        gameMessageHandler = __typ0
        rules = ''

        super(GameHandlerBotHandler, __tmp0).__init__(
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


handler_class = GameHandlerBotHandler
