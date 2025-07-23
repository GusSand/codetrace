from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from zulip_bots.game_handler import GameAdapter, BadMoveException
from typing import List, Any


class GameHandlerBotMessageHandler(object):
    tokens = [':blue_circle:', ':red_circle:']

    def __tmp8(__tmp0, __tmp1: __typ0) -> str:
        return 'foo'

    def __tmp9(__tmp0, __tmp2: <FILL>) :
        return __tmp0.tokens[__tmp2]

    def __tmp4(__tmp0, __tmp10: str, __tmp3) -> str:
        column_number = __tmp3.replace('move ', '')
        return __tmp10 + ' moved in column ' + column_number

    def game_start_message(__tmp0) -> str:
        return 'Type `move <column>` to place a token.\n \
The first player to get 4 in a row wins!\n \
Good Luck!'


class MockModel(object):
    def __init__(__tmp0) :
        __tmp0.current_board = 'mock board'

    def make_move(
        __tmp0,
        __tmp5: str,
        __tmp6: int,
        is_computer: bool=False
    ) :
        if not is_computer:
            if int(__tmp5.replace('move ', '')) < 9:
                return 'mock board'
            else:
                raise BadMoveException('Invalid Move.')
        return 'mock board'

    def __tmp7(__tmp0, players: List[str]) -> None:
        return None


class GameHandlerBotHandler(GameAdapter):
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
        model = MockModel
        gameMessageHandler = GameHandlerBotMessageHandler
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
